from django.test import TestCase

# Create your tests here.

FAILED_WORDS = (
   'Сделал', 'сделал', 'Дура', 'дура', 'Роботы', 'роботы'
)

# for i in range(len(FAILED_WORDS)):
#     sub_str = FAILED_WORDS[i][0:1] + '***'
#     print(sub_str)

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

