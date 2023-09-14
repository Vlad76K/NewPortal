from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, PostSearch, CategoryListView, subscribe, \
    SubscribeView
from django.views.decorators.cache import cache_page # импортируем декоратор для кэширования отдельного представления

app_name = 'newsportalapp'
urlpatterns = [
    # В данном случае путь ко всем постам у нас останется пустым.
    # Т.к. наше объявленное представление является классом, а Django ожидает функцию, нам надо представить этот
    # класс в виде view. Для этого вызываем метод as_view.
    path('', PostList.as_view(), name='post_list'),
    # pk — это первичный ключ поста, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path('<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),

    path('client_subscriber/', SubscribeView.as_view(), name='client_subscriber'),

    path('new/create/', PostCreate.as_view(), name='post_create'),
    path('new/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('new/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

    path('article/create/', PostCreate.as_view(), name='post_create'),
    path('article/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('article/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),

    # path('newsportalapp/', PostCreate.as_view(), name='newsportalapp'),
]

