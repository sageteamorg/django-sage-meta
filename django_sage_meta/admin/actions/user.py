from django.conf import settings
from django_sage_meta.models import UserData, FacebookPageData
from sage_meta.service import FacebookClient


def fetch_and_save_user_data(modeladmin, request, queryset):
    client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)

    client.account_handler.get_accounts()
    user_info = client.user_info
    user_data = UserData.objects.create(
        user_id=user_info.id,
        name=user_info.name,
        email=user_info.email,
        pages=FacebookPageData.objects.get(name=user_info.pages[0].name),
    )
    user_data.save()
    modeladmin.message_user(
        request, "User Data and Pages have been fetched and saved successfully."
    )


fetch_and_save_user_data.short_description = "Fetch and Save User Data from Facebook"
