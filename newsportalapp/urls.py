from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, PostSearch, Appointment

app_name = 'appointments'
urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым, чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом, а Django ожидает функцию, нам надо представить этот
    # класс в виде view. Для этого вызываем метод as_view.
    path('', PostList.as_view(), name='post_list'),
    # pk — это первичный ключ поста, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),

    path('new/create/', PostCreate.as_view(), name='post_create'),
    path('new/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('new/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

    path('article/create/', PostCreate.as_view(), name='post_create'),
    path('article/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('article/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

    path('appointments/', PostCreate.as_view(), name='appointments'),
]

