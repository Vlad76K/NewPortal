from django import forms
from django_filters import FilterSet, ModelMultipleChoiceFilter, CharFilter, DateFilter, RangeFilter, ModelChoiceFilter

# NumericRangeFilter #, ModelChoiceFilter
from .models import Post, Category, Author, User


# Создаем свой набор фильтров для модели Product.
class PostFilter(FilterSet):
    # Фильтр по автору поста
    post_author = ModelChoiceFilter(label='Автор заметки:', field_name='post_author_id',
                                    queryset=User.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}), )
    # Нечеткий поиск в заголовке (ищем вхождение указанного пользователем текста)
    post_title = CharFilter(label='Заголовок заметки:', field_name='post_title', lookup_expr='icontains')
    # Нечеткий поиск в заголовке (ищем вхождение указанного пользователем текста)
    post_text = CharFilter(label='Текст заметки:', field_name='post_text', lookup_expr='icontains')
    # Поиск рейтина по диапазону "от/до"
    post_rating = RangeFilter(label='Рейтинг заметки:', field_name='post_rating')
    # поиск по дате - вс посты в указанную дату и свежее
    post_date = DateFilter(label='Дата заметки:', field_name='post_date',
                           widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                           lookup_expr='gt')
    # Фильтр по категории поста. Предполагает фильтр по нескольким категориям
    post_category = ModelMultipleChoiceFilter(field_name='postcategory__category_connection',
        queryset=Category.objects.all(), label='Категория',
        conjoined=True  # в этом случае пост должен соответсвовать всем выбранным категориям
                        # для выбора "либо-либо", установить значение False
    )

    class Meta:
        # В Meta классе мы должны указать Django модель, в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели будет производиться фильтрация.
        fields = {
            'post_type': ['exact'],
        #     # поиск по заголовку
        #     'post_title': ['icontains'],
        #     'post_text': ['icontains'],
        #     'post_rating': [
        #         'lt',  # рейтинг должен быть меньше или равен указанному
        #         'gt',  # рейтинг должен быть больше или равен указанному
        #     ],
        }