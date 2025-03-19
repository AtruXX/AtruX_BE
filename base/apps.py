from django.apps import AppConfig
import os


class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'

    def ready(self):
        import atexit
        atexit.register(self.cleanup)

    def cleanup(self):
        if os.path.exists("/tmp/google_credentials.json"):
            os.remove("/tmp/google_credentials.json")
