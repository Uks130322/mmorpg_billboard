from django.apps import AppConfig


class AdvappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'advapp'

    def ready(self):
        """Add this configs in settings.py to plug the signals"""
        import advapp.signals
