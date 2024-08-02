import logging
from django.conf import settings
from django_sage_meta.models import FacebookPageData, Category
from sage_meta.service import FacebookClient

logger = logging.getLogger(__name__)


def fetch_and_save_pages(modeladmin, request, queryset):
    client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)

    pages = client.account_handler.get_accounts()

    page_objs = []
    instagram_business_account = None

    for page in pages:
        category = Category.objects.get(name=page.category)

        page_obj = FacebookPageData(
            page_id=page.id,
            name=page.name,
            categories=category,
            access_token=page.access_token,
            category=page.category,
            tasks=page.tasks,
            instagram_business_account=instagram_business_account,
        )
        page_objs.append(page_obj)
        print(page_obj)

    FacebookPageData.objects.bulk_create(page_objs)
    modeladmin.message_user(
        request,
        "Pages and Instagram business accounts have been fetched and saved successfully.",
    )


fetch_and_save_pages.short_description = "Fetch and Save Pages from Facebook"
