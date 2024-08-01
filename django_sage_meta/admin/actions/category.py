import logging
from sage_meta.service import FacebookClient
from django.conf import settings
from django.db import IntegrityError
from django_sage_meta.models import Category


logger = logging.getLogger(__name__)

def fetch_and_save_categories(modeladmin, request, queryset):
    # access_token = settings.FACEBOOK_ACCESS_TOKEN
    client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)

    accounts = client.account_handler.get_accounts()
    categories = []
    print(accounts)
    for account in accounts:
        for category in account.category_list:
            categories.append({'id': category.id, 'name': category.name})
    print(categories)
    category_objs = [
        Category(category_id=category['id'], name=category['name'])
        for category in categories
    ]

    Category.objects.bulk_create(category_objs, ignore_conflicts=True)

    modeladmin.message_user(request, "Categories have been fetched and saved successfully.")

fetch_and_save_categories.short_description = "Fetch and Save Categories from Facebook"
