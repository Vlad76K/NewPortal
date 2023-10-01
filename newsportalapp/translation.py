from .models import Post, Category
from modeltranslation.translator import register, TranslationOptions  # импортируем декоратор для перевода и класс
                                                                      # настроек, от которого будем наследоваться

# регистрируем наши модели для перевода
@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)  # указываем, какие именно поля надо переводить в виде кортежа
    # fields = ('name',)  # указываем, какие именно поля надо переводить в виде кортежа


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('post_title',)
    # fields = ('title',)