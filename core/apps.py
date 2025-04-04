from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        import core.signals  # سیگنال‌ها رو لود کن (فعلاً فایل signals.py رو نداریم)