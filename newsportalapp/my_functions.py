from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import mail_admins, EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string


# appointment_subject = '11111111111111'
# appointment_message = '22222222222222'
# recipient_list = ['Korwin@yandex.ru']
# send_mail(
#     # Категория и дата записи будут в теме для удобства
#     subject=appointment_subject,
#     # сообщение с кратким описанием
#     message=appointment_message,
#     # здесь указываете почту, с которой будете отправлять
#     from_email='Kornyushin.Vladislav@yandex.ru',
#     # здесь список получателей
#     recipient_list=recipient_list
# )


def mail_notification_pc(self, request, category, subscribecategory):
        # # отправляем письмо
        recipient_list = []
        qs_postcategory = request.POST['post_category']
        if int(qs_postcategory) > 0:
            _category_name = category.objects.filter(pk=qs_postcategory).values('category_name')
            qs_authorcategory = subscribecategory.objects.filter(category_connection=qs_postcategory).values('subscriber_connection')
            if qs_authorcategory.exists():
                for ac_id in qs_authorcategory[0].values():
                    qs_user = User.objects.filter(pk=ac_id).values('username', 'email', 'last_name', 'first_name')

                    # - И при добавлении новости из этой категории пользователю на email, указанный при регистрации, приходит письмо
                    # с HTML-кодом заголовка и первых 50 символов текста статьи.
                    #  --- В теме письма должен быть сам заголовок статьи.
                    #  --- Текст состоит из вышеуказанного HTML и текста: «Здравствуй, username. Новая статья в твоём любимом разделе!».

                    client_username = qs_user[0].get("username")  # логин подписчика
                    client_fname = qs_user[0].get("first_name")   # имя подписчика
                    client_lname = qs_user[0].get("last_name")    # фамилия подписчика
                    client_email = qs_user[0].get('email')        # почта подписчика
                    category_name = _category_name[0].get("category_name")  # наименование категории нового поста
                    # текст письма
                    appointment_message = f'Новые материалы в категории, на которую Вы подписаны: {category_name}! Приятного чтения!'
                    # тема письма
                    appointment_subject = f'Уважаемый, {client_fname}! Изменения в категории  {category_name} от {datetime.now()}'
                    # список адресов получателей рассылки
                    recipient_list.append(client_email)

                    # получаем наш html
                    html_content = render_to_string(
                        'post_create_notification.html',
                        {
                            'appointment_message': appointment_message,
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

                    # send_mail(
                    #     # Категория и дата записи будут в теме для удобства
                    #     subject=appointment_subject,
                    #     # сообщение с кратким описанием
                    #     message=appointment_message,
                    #     # здесь указываете почту, с которой будете отправлять
                    #     from_email='Kornyushin.Vladislav@yandex.ru',
                    #     # здесь список получателей
                    #     recipient_list=recipient_list
                    # )

                    # отправляем письмо всем админам по аналогии с send_mail, только здесь получателя указывать не надо
                    mail_admins(
                        subject=f'Клиенту {client_username} отправлено письмо: {appointment_subject}',
                        message=appointment_message,
                    )
        return HttpResponseRedirect(self.success_url, request)


@login_required
def subscribe(request, pk, category):
    user = request.user
    cat = category.objects.get(id=pk)
    cat.category_subscribe.add(user)

    message = f'Уважаемый, {user}! Вы успешно подписались на рассылку новостей в выбранных категориях!'
    return render(request, 'subscribe.html', {'category': cat, 'message': message})


# def create_post(request):
#     form = PostForm()
#
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('../')
#
#     return render(request, 'news_edit.html', {'form': form})


