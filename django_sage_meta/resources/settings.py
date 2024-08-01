from import_export import resources
from ..models import Settings


class SettingsResource(resources.ModelResource):
    class Meta:
        model = Settings
