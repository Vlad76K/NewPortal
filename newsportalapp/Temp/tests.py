# # Create your tests here.
# FAILED_WORDS = (
#    'Сделал', 'сделал', 'Дура', 'дура', 'Роботы', 'роботы'
# )
#
# # for i in range(len(FAILED_WORDS)):
# #     sub_str = FAILED_WORDS[i][0:1] + '***'
# #     print(sub_str)
#
# def censor(value):
#     """
#     value: значение, к которому нужно применить фильтр
#     """
#     if type(value) != str:
#         raise ValueError("Применять данный фильтр следует к строке!")
#
#     try:
#         # Возвращаемое функцией значение подставится в шаблон.
#         # value_new = value
#         value_list = value.split()
#         value_list_c = value_list.copy()
#
#         for i in range(len(FAILED_WORDS)):  # перебираем список запрещенных слов
#             j = 0
#             for value_list_word in value_list_c:            # перебираем слова из проверяемого текста
#                 if value_list_word == FAILED_WORDS[i]:     # если находим совпадение
#                     value_list_word_new = value_list_word[:1:1] + '*'*(len(value_list_word)-1)
#                     value_list.insert(j, value_list_word_new)
#                     value_list.pop(j+1)
#                 j += 1
#     except ValueError as error:
#         print(error)
#     else:
#         value_new = ' '.join(value_list)
#         return f'{value_new}'
#
# print(censor('«Фламенго» сделал первое, предложение? «Зениту» по сделал'))


# Поля объекта HTTPRequest:
#
# Имя поля	Что оно представляет?	Комментарий
# path	Путь к странице запроса	Пример: «news/post/create»
# method	Строка с именем HTTP-метода	«get», «post» и другие
# GET	Объект с данными GET-запроса	Представляет собой объект QueryDict
# POST	Объект с данными POST-запроса
# COOKIES	Словарь	Содержит описание всех поступивших куки
# session	Возвращает объект Session	Позволяет получить доступ к данным текущей сессии, из которой выполняется запрос
# user	Возвращает объект User	Содержит объект пользователя, который выполняет запрос. Может быть равен AnonimousUser