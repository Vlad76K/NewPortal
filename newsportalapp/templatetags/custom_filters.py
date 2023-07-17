from django import template

register = template.Library()

CURRENCIES_SYMBOLS = {
   'news': 'N',
   'articles': 'A',
}

FAILED_WORDS = (
   'Сделал', 'сделал', 'Дура', 'дура', 'Роботы', 'роботы'
)

# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
   """
   value: значение, к которому нужно применить фильтр
   """
   # Возвращаемое функцией значение подставится в шаблон.
   value_new = value
   for i in range(len(FAILED_WORDS)):
       sub_str = FAILED_WORDS[i][0:1] + '***'
       while str(value_new).find(FAILED_WORDS[i]) != -1:
           value_new = value_new.replace(FAILED_WORDS[i], sub_str)
   return f'{value_new}'

