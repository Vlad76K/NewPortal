import datetime

from celery import shared_task
import time

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, mail_admins
from django.template.loader import render_to_string

from .models import Post, SubscribeCategory


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)

@shared_task
def mail_notification_post_create(link, appointment_title, appointment_message, appointment_message1, appointment_subject, recipient_list, client_username):
    # получаем наш html
    html_content = render_to_string(
        'post_create_notification.html',
        {
            'link' : link,
            'post_title': appointment_title,
            'text': appointment_message,
            'text1': appointment_message1,
            'appointment_subject': appointment_subject,
        }
    )

    msg = EmailMultiAlternatives(
        # тема
        subject=appointment_subject,
        # сообщение с кратким описанием
        body=appointment_message,
        # почта, с которой будете отправлять
        from_email='Kornyushin.Vladislav@yandex.ru',
        # список получателей
        to=recipient_list,
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем

    # отправляем письмо всем админам по аналогии с send_mail, только здесь получателя указывать не надо
    mail_admins(
         subject=f'Клиенту {client_username} отправлено письмо: {appointment_subject}',
        message=appointment_message,
    )

@shared_task
def weekly_news(N):
    #  Your job processing logic here...
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)

    posts = Post.objects.filter(post_date__gte=last_week)
    posts_cat = posts.values_list('post_category', flat=True)
    categories = SubscribeCategory.objects.filter(category_connection_id__in=posts_cat).values_list("subscriber_connection_id", flat=True)
    subscribers = set(User.objects.filter(pk__in=categories).values_list('email', flat=True))

    html_context = render_to_string(
        'weekly_news.html', {
            # 'link': settings.SITE_URL,
            'link': 'http://127.0.0.1:8000/news/',
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        # from_email=settings.DEFAULT_FROM_EMAIL,
        from_email='Kornyushin.Vladislav@yandex.ru',
        to=subscribers,
    )
    msg.attach_alternative(html_context, 'text/html')
    msg.send()
