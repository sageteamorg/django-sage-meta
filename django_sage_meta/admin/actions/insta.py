import logging
from sage_meta.service import FacebookClient
from django.conf import settings
from django.db import IntegrityError
from django_sage_meta.models import InstagramAccount,Media,Insight,Story

logger = logging.getLogger(__name__)

def fetch_and_save_instagram_accounts(modeladmin, request, queryset):
    client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
    
    accounts = client.account_handler.get_accounts()
        
    insta_objs = []
    objs = []
    media_to_comments = []

    for account in accounts:
        media_obj = Media.objects.filter(username=account.instagram_business_account.username)
        insta_obj = InstagramAccount(
                    account_id=account.instagram_business_account.id,
                    username=account.instagram_business_account.username,
                    follows_count=account.instagram_business_account.follows_count,
                    followers_count=account.instagram_business_account.followers_count,
                    media_count=account.instagram_business_account.media_count,
                    profile_picture_url=account.instagram_business_account.profile_picture_url,
                    website=account.instagram_business_account.website,
                    biography=account.instagram_business_account.biography,
        )
        insta_objs.append(insta_obj)
    
        objs.append((insta_obj, media_obj))
    
    InstagramAccount.objects.bulk_create(insta_objs, ignore_conflicts=True)


    for insta, medias in objs:
        insta_j = InstagramAccount.objects.get(username=insta.username)
        media_objs = Media.objects.filter(media_id__in=[media.media_id for media in medias])
        insta_j.media.set(media_objs)
    modeladmin.message_user(request, "Media and comments have been fetched and saved successfully.")

fetch_and_save_instagram_accounts.short_description = "Fetch and Save Instagram Business Accounts from Facebook"
