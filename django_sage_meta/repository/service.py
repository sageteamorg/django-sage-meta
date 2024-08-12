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
from django_sage_meta.helper.choice import ContentFileEnum
from django.db import transaction

from sage_meta.service import FacebookClient

logger = logging.getLogger(__name__)


class SyncService:
    """Service class to handle synchronization of data from Facebook and
    Instagram to the local database."""

    @staticmethod
    def sync_instagram_accounts():
        """Sync Instagram account data including media items associated with
        each account."""
        client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
        accounts = client.account_handler.get_accounts()

        insta_objs, objs = SyncService._process_instagram_accounts(accounts)

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
        logger.info(objs)

        # for insta, medias in objs:
        #     insta_j = InstagramAccount.objects.get(username=insta.username)
        #     media_objs = Media.objects.filter(
        #         media_id__in=[media.media_id for media in medias]
        #     )
        #     insta_j.media.set(media_objs)

    @staticmethod
    def sync_facebook_pages():
        """Sync Facebook page data including categories and associated
        Instagram business accounts."""
        client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
        pages = client.account_handler.get_accounts()
        user_info = client.user_info
        page_objs = SyncService._process_facebook_pages(pages, user_info)

        SyncService._bulk_sync(
            page_objs,
            FacebookPageData,
            [
                "name",
                "category",
                "access_token",
                "tasks",
                "instagram_business_account_id",
            ],
        )

    @staticmethod
    def sync_insights():
        """Sync Instagram insights data."""
        client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
        insights = client.media_handler.get_instagram_insights(settings.INSTA_ID)

        insight_objs = SyncService._process_insights(insights)

        SyncService._bulk_sync(
            insight_objs, Insight, ["name", "period", "values", "title", "description"]
        )

    @staticmethod
    def sync_user_data():
        """Sync user data including associated Facebook pages."""
        client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
        client.account_handler.get_accounts()
        user_info = client.user_info

        UserData.objects.update_or_create(
            user_id=user_info.id,
            defaults={"name": user_info.name, "email": user_info.email},
        )

    @staticmethod
    def sync_categories():
        """Sync category data from Facebook accounts."""
        client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
        accounts = client.account_handler.get_accounts()

        category_objs = SyncService._process_categories(accounts)

        SyncService._bulk_sync(category_objs, Category, ["name"])

    @staticmethod
    def sync_media():
        """Sync media data including associated comments."""
        client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
        media_list = client.media_handler.get_instagram_media(settings.INSTA_ID)

        media_objs, all_comment_objs, media_to_comments = SyncService._process_media(
            media_list, client
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

    @staticmethod
    def sync_stories():
        """Sync Instagram stories."""
        client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
        stories = client.story_handler.get_instagram_stories(settings.INSTA_ID)

        story_objs = SyncService._process_stories(stories)

        SyncService._bulk_sync(story_objs, Story)

    @staticmethod
    def _bulk_sync(objs, model, update_fields=None):
        """Helper method to handle bulk create and update operations.

        Args:
            objs (list): List of objects to be created or updated.
            model (Model): Django model to perform operations on.
            update_fields (list): List of fields to update in case of existing records.

        """
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
        except Exception as e:
            raise Exception(f"Error during bulk synchronization: {e}")

    @staticmethod
    def _process_instagram_accounts(accounts):
        """Process Instagram accounts to prepare for bulk synchronization.

        Args:
            accounts (list): List of Instagram accounts.

        Returns:
            tuple: List of InstagramAccount objects, List of tuples containing InstagramAccount and associated Media objects.

        """
        insta_objs = []
        objs = []
        for account in accounts:
            insta_account = account.instagram_business_account
            if not insta_account:
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

        return insta_objs, objs

    @staticmethod
    def _process_facebook_pages(pages, user_info):
        """Process Facebook pages to prepare for bulk synchronization.

        Args:
            pages (list): List of Facebook pages.

        Returns:
            list: List of FacebookPageData objects.

        """
        existing_pages_dict = {p.page_id: p for p in FacebookPageData.objects.all()}

        page_objs = []
        for page in pages:
            category = Category.objects.get(name=page.category)
            page_obj = existing_pages_dict.get(page.id)
            user_obj = UserData.objects.get(name=user_info.name)
            insta_obj = InstagramAccount.objects.get(account_id=settings.INSTA_ID)
            if page_obj:
                if (
                    page_obj.name != page.name
                    or page_obj.category != category
                    or page_obj.access_token != page.access_token
                    or page_obj.tasks != page.tasks
                    or page.user_id
                    or page_obj.instagram_business_account_id
                    != page.instagram_business_account
                ):
                    page_obj.name = page.name
                    page_obj.category = category
                    page_obj.access_token = page.access_token
                    page_obj.tasks = page.tasks
                    page_obj.user = user_obj
                    page_obj.instagram_business_account_id = (
                        page.instagram_business_account
                    )
                    page_objs.append(page_obj)
            else:
                page_obj = FacebookPageData(
                    page_id=page.id,
                    name=page.name,
                    category=category,
                    access_token=page.access_token,
                    tasks=page.tasks,
                    instagram_business_account=insta_obj,
                    user=user_obj,
                )
                page_objs.append(page_obj)

        return page_objs

    @staticmethod
    def _process_insights(insights):
        """Process Instagram insights to prepare for bulk synchronization.

        Args:
            insights (list): List of Instagram insights.

        Returns:
            list: List of Insight objects.

        """
        existing_insights_dict = {i.insight_id: i for i in Insight.objects.all()}
        insight_objs = []

        for insight in insights:
            insight_obj = existing_insights_dict.get(insight.id)
            insta_obj = InstagramAccount.objects.get(account_id=settings.INSTA_ID)
            if insight_obj:
                if (
                    insight_obj.name != insight.name
                    or insight_obj.period != insight.period
                    or insight_obj.values != insight.values
                    or insight_obj.title != insight.title
                    or insight_obj.account != insight.account
                    or insight_obj.description != insight.description
                ):
                    insight_obj.name = insight.name
                    insight_obj.period = insight.period
                    insight_obj.values = insight.values
                    insight_obj.title = insight.title
                    insight_obj.description = insight.description
                    insight_obj.account = insight.account

                    insight_objs.append(insight_obj)
            else:
                insight_obj = Insight(
                    insight_id=insight.id,
                    name=insight.name,
                    period=insight.period,
                    values=insight.values,
                    title=insight.title,
                    description=insight.description,
                    account=insta_obj,
                )
                insight_objs.append(insight_obj)

        return insight_objs

    @staticmethod
    def _process_categories(accounts):
        """Process categories to prepare for bulk synchronization.

        Args:
            accounts (list): List of Facebook accounts.

        Returns:
            list: List of Category objects.

        """
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
            else:
                category_obj = Category(
                    category_id=category["id"], name=category["name"]
                )
                category_objs.append(category_obj)

        return category_objs

    @staticmethod
    def _process_media(media_list, client):
        """Process media items to prepare for bulk synchronization.

        Args:
            media_list (list): List of media items.
            client (FacebookClient): Instance of FacebookClient.

        Returns:
            tuple: List of Media objects, List of Comment objects, List of tuples containing media IDs and comment IDs.

        """
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
                else:
                    comment_obj = Comment(
                        comment_id=comment.id,
                        text=comment.text,
                        username=comment.username,
                        like_counts=comment.like_count,
                        timestamp=comment.timestamp,
                    )
                    all_comment_objs.append(comment_obj)

                comment_objs.append(comment_obj)
                media_to_comments.append((media.id, comment.id))

        return media_objs, all_comment_objs, media_to_comments

    @staticmethod
    def _process_stories(stories):
        """Process stories to prepare for bulk synchronization.

        Args:
            stories (list): List of stories.

        Returns:
            list: List of Story objects.

        """
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

        return story_objs


class PublisherService:
    """Service class for publishing media, stories, and comments to Facebook.

    This class handles the publishing of different types of content to
    Facebook using the FacebookClient. It includes methods for
    publishing media, stories, and comments, and provides error handling
    and logging for these operations.

    """

    def __init__(self):
        """Initializes the PublisherService.

        This method initializes the FacebookClient with the access token
        from settings and retrieves the accounts associated with the
        client.

        """
        self.client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
        self.client.account_handler.get_accounts()

    def publish_media(self, media):
        """Publishes a media object to Facebook.

        This method publishes a media object based on its type. If the media is an image and
        is part of a carousel, it publishes the carousel. Otherwise, it publishes the photo
        or video.

        Args:
            media (Media): The media object to be published.

        """
        try:
            if media.kind == "image":
                if media.carousel:
                    carousel_list = media.media_url.split(",")
                    self.client.content_publisher.publish_carousel(
                        carousel_list, media.caption
                    )
                else:
                    self.client.content_publisher.publish_photo(
                        media.media_url, media.caption
                    )
            else:
                self.client.content_publisher.publish_video(media.media_url)
            logger.info(f"Successfully published media with ID {media.id}")
        except Exception as e:
            logger.error(f"Failed to publish media with ID {media.id}: {e}")
            raise

    def handle_publish(self, queryset):
        """Publishes a queryset of media objects to Facebook.

        This method iterates over a queryset of media objects and attempts to publish each
        one. It logs the success or failure of each publication attempt.

        Args:
            queryset (QuerySet): The queryset of media objects to be published.

        """
        for media in queryset:
            try:
                self.publish_media(media)
            except Exception as e:
                logger.error(f"Failed to publish media with ID {media.id}: {e}")
                raise

    def publish_story(self, story):
        """Publishes a story object to Facebook.

        This method publishes a story object to Facebook and logs the success or failure
        of the publication attempt.

        Args:
            story (Story): The story object to be published.

        """
        try:
            self.client.content_publisher.publish_story(story.media_url)
            logger.info(f"Successfully published story: {story.media_url}")
        except Exception as e:
            logger.error(f"Failed to publish story: {e}")
            raise

    def publish_comment(self, comment):
        """Publishes a comment object to Facebook.

        This method publishes a comment object to Facebook, linking it to the corresponding
        media, and logs the success or failure of the publication attempt.

        Args:
            comment (Comment): The comment object to be published.

        """
        try:
            self.client.content_publisher.put_comment(
                comment.media.media_id, comment.text
            )
            logger.info(f"Successfully published comment: {comment.comment_id}")
        except Exception as e:
            logger.error(f"Failed to publish comment: {e}")
            raise
