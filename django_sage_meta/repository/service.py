import logging
from django.conf import settings
from django_sage_meta.models import (
    UserData,
    FacebookPageData,
    InstagramAccount,
    Insight,
    Category,
    Media,
    Comment,
    Story,
)
from django_sage_meta.helper.choice import ContentFileEnum, InsightKindEnum
from django.db import transaction
from sage_meta.service import FacebookClient

logger = logging.getLogger(__name__)


class SyncService:
    """Service class to handle synchronization of data from Facebook and
    Instagram to the local database."""

    @staticmethod
    def sync_instagram_accounts():
        logger.info("Starting sync of Instagram accounts...")
        client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
        accounts = client.account_handler.get_accounts()
        logger.debug(f"Fetched {len(accounts)} Instagram accounts from Facebook.")

        insta_objs, objs = SyncService._process_instagram_accounts(accounts)
        logger.debug(f"Processed {len(insta_objs)} Instagram accounts for sync.")

        SyncService._bulk_sync(
            insta_objs,
            InstagramAccount,
            [
                "username",
                "follows_counts",
                "followers_counts",
                "media_counts",
                "profile_picture_url",
                "website",
                "biography",
            ],
        )
        logger.info("Instagram accounts sync completed.")

    @staticmethod
    def sync_facebook_pages():
        logger.info("Starting sync of Facebook pages...")
        client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
        pages = client.account_handler.get_accounts()
        user_info = client.user_info
        logger.debug(f"Fetched {len(pages)} Facebook pages.")

        page_objs, page_to_categories = SyncService._process_facebook_pages(
            pages, user_info
        )
        logger.debug(f"Processed {len(page_objs)} Facebook pages for sync.")

        SyncService._bulk_sync(
            page_objs,
            FacebookPageData,
            [
                "name",
                "access_token",
                "tasks",
                "instagram_business_account",
            ],
        )
        for page, category in page_to_categories:
            if page.pk:
                page.categories.set(category)
                logger.debug(f"Set categories for page {page.page_id}.")

        logger.info("Facebook pages sync completed.")

    @staticmethod
    def sync_insights(kind=0, insights_object=None, media_id=None):
        logger.info(f"Starting sync of Instagram insights, kind={kind}...")
        client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
        media_obj = None
        if kind == 0:
            insights = client.media_handler.get_instagram_insights(settings.INSTA_ID)
        else:
            insights = insights_object
            media_obj = media_id

        logger.debug(f"Fetched insights for kind={kind} with media_id={media_id}.")

        insight_objs = SyncService._process_insights(insights, kind, media_obj)
        logger.debug(f"Processed {len(insight_objs)} insights for sync.")

        SyncService._bulk_sync(
            insight_objs, Insight, ["name", "period", "values", "title", "description"]
        )
        logger.info("Instagram insights sync completed.")

    @staticmethod
    def sync_user_data():
        logger.info("Starting sync of user data...")
        client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
        client.account_handler.get_accounts()
        user_info = client.user_info
        logger.debug(f"Fetched user data: {user_info.name} (ID: {user_info.id}).")

        UserData.objects.update_or_create(
            user_id=user_info.id,
            defaults={"name": user_info.name, "email": user_info.email},
        )
        logger.info("User data sync completed.")

    @staticmethod
    def sync_categories():
        logger.info("Starting sync of categories...")
        client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
        accounts = client.account_handler.get_accounts()
        logger.debug("Fetched accounts for category sync.")

        category_objs = SyncService._process_categories(accounts)
        logger.debug(f"Processed {len(category_objs)} categories for sync.")

        SyncService._bulk_sync(category_objs, Category, ["name"])
        logger.info("Categories sync completed.")

    @staticmethod
    def sync_media():
        logger.info("Starting sync of media...")
        client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
        media_list = client.media_handler.get_instagram_media(settings.INSTA_ID)
        logger.debug(f"Fetched {len(media_list)} media items from Instagram.")

        media_objs, all_comment_objs, media_to_comments = SyncService._process_media(
            media_list, client
        )
        logger.debug(
            f"Processed {len(media_objs)} media items and {len(all_comment_objs)} comments for sync."
        )

        SyncService._bulk_sync(
            media_objs,
            Media,
            [
                "username",
                "caption",
                "kind",
                "media_url",
                "timestamp",
                "like_counts",
                "comments_counts",
            ],
        )
        SyncService._bulk_sync(
            all_comment_objs, Comment, ["text", "username", "like_counts", "timestamp"]
        )

        for media_id, comment_id in media_to_comments:
            media_obj = Media.objects.get(media_id=media_id)
            comment_obj = Comment.objects.get(comment_id=comment_id)
            comment_obj.media = media_obj
            comment_obj.save()
            logger.debug(f"Linked comment {comment_id} to media {media_id}.")

        logger.info("Media sync completed.")

    @staticmethod
    def sync_stories():
        logger.info("Starting sync of Instagram stories...")
        client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
        stories = client.story_handler.get_instagram_stories(settings.INSTA_ID)
        logger.debug(f"Fetched {len(stories)} stories from Instagram.")

        story_objs = SyncService._process_stories(stories)
        logger.debug(f"Processed {len(story_objs)} stories for sync.")

        SyncService._bulk_sync(story_objs, Story)
        logger.info("Instagram stories sync completed.")

    @staticmethod
    def _bulk_sync(objs, model, update_fields=None):
        logger.debug(
            f"Starting bulk sync for model {model.__name__} with {len(objs)} objects."
        )
        try:
            with transaction.atomic():
                batch_size = 1000
                for i in range(0, len(objs), batch_size):
                    model.objects.bulk_create(
                        [obj for obj in objs[i : i + batch_size] if not obj.pk],
                        ignore_conflicts=True,
                    )
                    if update_fields:
                        model.objects.bulk_update(
                            [obj for obj in objs[i : i + batch_size] if obj.pk],
                            update_fields,
                        )
                logger.debug(f"Bulk sync for model {model.__name__} completed.")
        except Exception as e:
            logger.error(f"Error during bulk synchronization: {e}")
            raise

    @staticmethod
    def _process_instagram_accounts(accounts):
        logger.debug("Processing Instagram accounts for sync.")
        insta_objs = []
        objs = []
        for account in accounts:
            insta_account = account.instagram_business_account
            if not insta_account:
                logger.debug("Skipping account without Instagram business account.")
                continue

            media_obj = Media.objects.filter(username=insta_account.username)
            insta_obj = InstagramAccount(
                account_id=insta_account.id,
                username=insta_account.username,
                follows_counts=insta_account.follows_count,
                followers_counts=insta_account.followers_count,
                media_counts=insta_account.media_count,
                profile_picture_url=insta_account.profile_picture_url,
                website=insta_account.website,
                biography=insta_account.biography,
            )
            insta_objs.append(insta_obj)
            objs.append((insta_obj, media_obj))

        logger.debug(f"Processed {len(insta_objs)} Instagram accounts for bulk sync.")
        return insta_objs, objs

    @staticmethod
    def _process_facebook_pages(pages, user_info):
        logger.debug("Processing Facebook pages for sync.")
        existing_pages_dict = {p.page_id: p for p in FacebookPageData.objects.all()}

        page_objs = []
        page_to_categories = []
        for page in pages:
            categories = Category.objects.filter(name=page.category)
            page_obj = existing_pages_dict.get(page.id)
            user_obj = UserData.objects.get(name=user_info.name)
            insta_obj = InstagramAccount.objects.get(account_id=settings.INSTA_ID)
            if page_obj:
                if page_obj.name != page.name or page_obj.tasks != page.tasks:
                    page_obj.name = page.name
                    page_obj.tasks = page.tasks
                    page_obj.user = user_obj
                    page_obj.instagram_business_account = (
                        page.instagram_business_account
                    )
                    page_objs.append(page_obj)
                    logger.debug(f"Updated existing page {page.id}.")
            else:
                page_obj = FacebookPageData(
                    page_id=page.id,
                    name=page.name,
                    access_token=page.access_token,
                    tasks=page.tasks,
                    instagram_business_account=insta_obj,
                    user=user_obj,
                )
                page_objs.append(page_obj)
                page_to_categories.append((page_obj, categories))
                logger.debug(f"Created new page {page.id}.")

        logger.debug(f"Processed {len(page_objs)} Facebook pages for bulk sync.")
        return page_objs, page_to_categories

    @staticmethod
    def _process_insights(insights, kind=0, media_id=None):
        logger.debug("Processing Instagram insights for sync.")
        existing_insights_dict = {i.insight_id: i for i in Insight.objects.all()}
        insight_objs = []
        insta_obj = None
        media_obj = None
        for insight in insights:
            insight_obj = existing_insights_dict.get(insight.id)
            if kind == 0:
                insta_obj = InstagramAccount.objects.get(account_id=settings.INSTA_ID)
                insight_kind = InsightKindEnum.account
            else:
                media_obj = Media.objects.filter(media_id=media_id).first()
                insight_kind = InsightKindEnum.media

            if insight_obj:
                if (
                    insight_obj.name != insight.name
                    or insight_obj.period != insight.period
                    or insight_obj.values != insight.values
                    or insight_obj.title != insight.title
                    or insight_obj.description != insight.description
                    or insight_obj.kind != insight_kind
                ):
                    insight_obj.name = insight.name
                    insight_obj.period = insight.period
                    insight_obj.values = insight.values
                    insight_obj.title = insight.title
                    insight_obj.description = insight.description
                    insight_obj.account = insight.account
                    insight_obj.media = media_obj
                    insight_obj.kind = insight_kind

                    insight_objs.append(insight_obj)
                    logger.debug(f"Updated existing insight {insight.id}.")
            else:
                insight_obj = Insight(
                    insight_id=insight.id,
                    name=insight.name,
                    period=insight.period,
                    values=insight.values,
                    media=media_obj,
                    title=insight.title,
                    kind=insight_kind,
                    description=insight.description,
                    account=insta_obj,
                )
                insight_objs.append(insight_obj)
                logger.debug(f"Created new insight {insight.id}.")

        logger.debug(f"Processed {len(insight_objs)} insights for bulk sync.")
        return insight_objs

    @staticmethod
    def _process_categories(accounts):
        logger.debug("Processing categories for sync.")
        categories = []
        for account in accounts:
            for category in account.category_list:
                categories.append({"id": category.id, "name": category.name})

        existing_categories_dict = {c.category_id: c for c in Category.objects.all()}
        category_objs = []

        for category in categories:
            category_obj = existing_categories_dict.get(category["id"])
            if category_obj:
                if category_obj.name != category["name"]:
                    category_obj.name = category["name"]
                    category_objs.append(category_obj)
                    logger.debug(f"Updated existing category {category['id']}.")
            else:
                category_obj = Category(
                    category_id=category["id"], name=category["name"]
                )
                category_objs.append(category_obj)
                logger.debug(f"Created new category {category['id']}.")

        logger.debug(f"Processed {len(category_objs)} categories for bulk sync.")
        return category_objs

    @staticmethod
    def _process_media(media_list, client):
        logger.debug("Processing media items for sync.")
        existing_media_dict = {m.media_id: m for m in Media.objects.all()}
        existing_comment_dict = {c.comment_id: c for c in Comment.objects.all()}
        media_objs = []
        all_comment_objs = []
        media_to_comments = []

        for media in media_list:
            kind = (
                ContentFileEnum.image
                if media.media_type == "IMAGE"
                else ContentFileEnum.videos
            )
            media_obj = existing_media_dict.get(media.id)
            account_insta = InstagramAccount.objects.get(username=media.username)
            if media_obj:
                if (
                    media_obj.username != media.username
                    or media_obj.caption != media.caption
                    or media_obj.kind != kind
                    or media_obj.media_url != media.media_url
                    or media_obj.timestamp != media.timestamp
                    or media_obj.like_counts != media.like_count
                    or media_obj.comments_counts != media.comments_count
                    or media_obj.account != account_insta
                ):
                    media_obj.username = media.username
                    media_obj.caption = media.caption
                    media_obj.kind = kind
                    media_obj.media_url = media.media_url
                    media_obj.timestamp = media.timestamp
                    media_obj.like_counts = media.like_count
                    media_obj.comments_counts = media.comments_count
                    media_obj.account = account_insta
                    media_objs.append(media_obj)
                    logger.debug(f"Updated existing media {media.id}.")
            else:
                media_obj = Media(
                    username=media.username,
                    media_id=media.id,
                    caption=media.caption,
                    kind=kind,
                    media_url=media.media_url,
                    timestamp=media.timestamp,
                    like_counts=media.like_count,
                    comments_counts=media.comments_count,
                    account=account_insta,
                )
                media_objs.append(media_obj)
                logger.debug(f"Created new media {media.id}.")

            comments = client.comment_handler.get_instagram_comments(media.id)
            comment_objs = []
            for comment in comments:
                comment_obj = existing_comment_dict.get(comment.id)
                if comment_obj:
                    if (
                        comment_obj.text != comment.text
                        or comment_obj.username != comment.username
                        or comment_obj.like_counts != comment.like_count
                        or comment_obj.timestamp != comment.timestamp
                    ):
                        comment_obj.text = comment.text
                        comment_obj.username = comment.username
                        comment_obj.like_counts = comment.like_count
                        comment_obj.timestamp = comment.timestamp
                        all_comment_objs.append(comment_obj)
                        logger.debug(f"Updated existing comment {comment.id}.")
                else:
                    comment_obj = Comment(
                        comment_id=comment.id,
                        text=comment.text,
                        username=comment.username,
                        like_counts=comment.like_count,
                        timestamp=comment.timestamp,
                    )
                    all_comment_objs.append(comment_obj)
                    logger.debug(f"Created new comment {comment.id}.")

                comment_objs.append(comment_obj)
                media_to_comments.append((media.id, comment.id))
                logger.debug(f"Linked comment {comment.id} to media {media.id}.")

            insights = client.media_handler.get_media_insights(media.id)
            SyncService.sync_insights(1, insights, media.id)

        logger.debug(
            f"Processed {len(media_objs)} media items and {len(all_comment_objs)} comments for bulk sync."
        )
        return media_objs, all_comment_objs, media_to_comments

    @staticmethod
    def _process_stories(stories):
        logger.debug("Processing stories for sync.")
        story_objs = []
        for story in stories:
            account_insta = InstagramAccount.objects.get(username=story.username)
            story_objs.append(
                Story(
                    story_id=story.id,
                    media_type=story.media_type,
                    media_url=story.media_url,
                    timestamp=story.timestamp,
                    account=account_insta,
                )
            )
            logger.debug(f"Processed story {story.id} for sync.")

        logger.debug(f"Processed {len(story_objs)} stories for bulk sync.")
        return story_objs


class PublisherService:
    """Service class for publishing media, stories, and comments to Facebook.

    This class handles the publishing of different types of content to
    Facebook using the FacebookClient. It includes methods for
    publishing media, stories, and comments, and provides error handling
    and logging for these operations.

    """

    def __init__(self):
        logger.info("Initializing PublisherService...")
        self.client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
        self.client.account_handler.get_accounts()
        logger.info("PublisherService initialized.")

    def publish_media(self, media):
        logger.info(f"Publishing media with ID {media.id}...")
        try:
            if media.kind == "image":
                if media.carousel:
                    carousel_list = media.media_url.split(",")
                    self.client.content_publisher.publish_carousel(
                        carousel_list, media.caption
                    )
                    logger.debug(f"Published image carousel for media {media.id}.")
                else:
                    self.client.content_publisher.publish_photo(
                        media.media_url, media.caption
                    )
                    logger.debug(f"Published photo for media {media.id}.")
            else:
                self.client.content_publisher.publish_video(media.media_url)
                logger.debug(f"Published video for media {media.id}.")
            logger.info(f"Successfully published media with ID {media.id}.")
        except Exception as e:
            logger.error(f"Failed to publish media with ID {media.id}: {e}")
            raise

    def handle_publish(self, queryset):
        logger.info("Starting batch publish for media queryset...")
        for media in queryset:
            try:
                self.publish_media(media)
            except Exception as e:
                logger.error(f"Failed to publish media with ID {media.id}: {e}")
                raise
        logger.info("Batch publish completed.")

    def publish_story(self, story):
        logger.info(f"Publishing story with ID {story.story_id}...")
        try:
            self.client.content_publisher.publish_story(story.media_url)
            logger.info(f"Successfully published story: {story.media_url}.")
        except Exception as e:
            logger.error(f"Failed to publish story: {e}")
            raise

    def publish_comment(self, comment):
        logger.info(f"Publishing comment with ID {comment.comment_id}...")
        try:
            self.client.content_publisher.put_comment(
                comment.media.media_id, comment.text
            )
            logger.info(f"Successfully published comment: {comment.comment_id}.")
        except Exception as e:
            logger.error(f"Failed to publish comment: {e}")
            raise
