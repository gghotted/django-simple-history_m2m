from django.apps import AppConfig


class SimpleHistoryM2MConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simple_history_m2m'

    def ready(self):
        from simple_history_m2m import signals
