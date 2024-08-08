from django.apps import AppConfig


class DjangoSageFacebookConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_sage_meta"
    def ready(self):
        import django_sage_meta.signals
