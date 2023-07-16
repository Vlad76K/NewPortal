from django import template

register = template.Library()

CURRENCIES_SYMBOLS = {
   'news': 'N',
   'articles': 'A',
}

# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def post_type_filter(value, code='N'):
   """
   value: значение, к которому нужно применить фильтр
   """
   # Возвращаемое функцией значение подставится в шаблон.
   # if value == 'N':
   #    return True
   postfix = CURRENCIES_SYMBOLS[code]
   return f'{value} {postfix}'