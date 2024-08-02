from import_export import resources
from ..models import UserData


class UserDataResource(resources.ModelResource):
    class Meta:
        model = UserData
