import requests_oauthlib
from allauth.account.forms import SignupForm
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelMultipleChoiceField

from .models import Post, User, Category, SubscribeCategory

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class PostForm(forms.ModelForm):
    post_text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        # fields = '__all__'
        fields = ['post_author', 'post_title', 'post_text', 'post_category', 'post_rating', ]

    def clean(self):
        cleaned_data = super().clean()
        post_text = cleaned_data.get('post_text')
        post_title = cleaned_data.get('post_title')
        if str(post_text) == str(post_title):
            raise ValidationError({
                'post_title': "Заголовок не должен быть идентичен тексту."
            })

        return cleaned_data

# Тест работы проверок через python manage.py shell
# from newsportalapp.forms import PostForm
# f = PostForm({'post_text': 'test', 'post_category': [1], 'post_author': 2, 'post_title': 'test', 'post_rating': 1})
# f.errors


class SubscribeForm(forms.ModelForm):
    # !!!!!!!!!!!!!!!!!!!!  НАДО СУМЕТЬ ПОЛУЧИТЬ id ПОЛЬЗОВАТЕЛЯ  !!!!!!!!!!!!!!!!!!!!
    subscriber_connection = User.objects.filter(pk=1).values('username')
    category_connection = ModelMultipleChoiceField(queryset=Category.objects.all(),
                                                   label='Категория',
                                                   to_field_name='id',  # 'category_name',
                                                   widget=forms.CheckboxSelectMultiple())

    class Meta:
        # В Meta классе мы должны указать Django модель с которой будем работать
        model = SubscribeCategory
        # В fields мы описываем набор нужных нам полей
        # fields = '__all__'  # не желательный формат записи - лучше делать явное перечисление полей. Но для начала сойдет
        fields = ['subscriber_connection', 'category_connection', ]

    def get_sub_con(self):
        return f"Выберите интересующие Вас категории для оформления подписки!"
        # for value in self.subscriber_connection:
        #     return f"Уважаемый {value.get('username')}! Выберите интересующие Вас категории для оформления подписки!"
        # return '- Неидентифицированный пользователь! -'

# from newsportalapp.forms import SubscribeForm
# f = SubscribeForm({'subscribe_category': [1], 'subscribe_user': 2})
# f.errors


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)

        return user

