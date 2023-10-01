from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment
from modeltranslation.admin import TranslationAdmin  # импортируем модель амдинки (вспоминаем модуль про
                                                     # переопределение стандартных админ-инструментов)

# Register your models here.
# Регистрируем модели для перевода в админке
class CategoryAdmin(TranslationAdmin):
    model = Category

class PostAdmin(TranslationAdmin):
    model = Post

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Category)
