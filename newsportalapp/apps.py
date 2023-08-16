from django.apps import AppConfig

class NewsportalappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsportalapp'

    def ready(self):
        # from .signals import notify_managers_appointment
        # from .tasks import send_mails
        # from .scheduler import newsportalapp_scheduler
        # from .management.commands import runapscheduler
        #
        # runapscheduler.my_job()

        # print('started')
        # newsportalapp_scheduler.add_job(
        #     id='mail_send',
        #     func=send_mails,
        #     trigger='interval',
        #     seconds=10,
        # )
        # newsportalapp_scheduler.start()
        # notify_managers_appointment
        pass