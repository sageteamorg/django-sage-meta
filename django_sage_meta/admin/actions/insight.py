import logging
from sage_meta.service import FacebookClient
from django.conf import settings
from django_sage_meta.models import Insight

logger = logging.getLogger(__name__)


def fetch_and_save_insights(modeladmin, request, queryset):
    client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)

    insights = client.media_handler.get_instagram_insights(settings.INSTA_ID)
    print(insights)
    insight_objs = [
        Insight(
            insight_id=insight.id,
            name=insight.name,
            period=insight.period,
            values=insight.values,
            title=insight.title,
            description=insight.description,
        )
        for insight in insights
    ]

    Insight.objects.bulk_create(insight_objs, ignore_conflicts=True)
    modeladmin.message_user(
        request, "Insights have been fetched and saved successfully."
    )


fetch_and_save_insights.short_description = "Fetch and Save Insights from Facebook"
