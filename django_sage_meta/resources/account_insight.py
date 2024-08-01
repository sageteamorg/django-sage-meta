from import_export import resources
from ..models import AccountInsight


class AccountInsightResource(resources.ModelResource):
    class Meta:
        model = AccountInsight
