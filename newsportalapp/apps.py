from django.apps import AppConfig


class NewsportalappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsportalapp'

    # def ready(self):
    #     import NewsPortal_django.newsportalapp.signals