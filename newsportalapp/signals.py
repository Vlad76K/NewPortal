from django.conf import settings
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPortal_django.newsportalapp.models import Post


# создаём функцию-обработчик с параметрами под регистрацию сигнала
@receiver(post_save, sender=Post)
def notify_managers_appointment(sender, instance, created, **kwargs):
    subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
    mail_managers(
        subject=subject,
        message=instance.message,
    )


def send_notification(preview, pk, title, subscribers):
    html_context = render_to_string("news/account/email/post_created_email.html",
                                    {"text": preview, "link": f"{settings.SITE_URL}/news/post/{pk}"})
    msg = EmailMultiAlternatives(subject=title, body="", from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers, )
    msg.attach_alternative(html_context, "text/html")
    msg.send()


@receiver(m2m_changed, sender=Post.post_category.through)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.post_category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notification(instance.preview(), instance.pk, instance.title, subscribers)
