from django import forms
from django.core.exceptions import ValidationError

from .models import Post

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

