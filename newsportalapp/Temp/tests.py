# Импортировать пакет psycopg2
import psycopg2

# Открыть подключение к базе.
# Обратите внимание на синтаксис строки с информацией о БД:
# если вы меняли настройки своей БД, то и здесь им придётся
# указать соответствующие.
# Кстати, таких подключений можно открывать сколько угодно:
# вдруг у вашего приложения данные распределены
# по нескольким базам?
conn = psycopg2.connect(dbname="postgres", host="localhost", user="postgres", password="A123456", port="5433")

# Создать «курсор» на подключении к базе.
# Курсоры используются для представления
# сессий подключения к БД.
cur = conn.cursor()

# Выполнить команду напрямую.
cur.execute(
    "CREATE TABLE test12 (id serial PRIMARY KEY, num integer, data varchar);"
)

# Выполнить команду, не заботясь о корректном синтаксисе
# представления данных: psycopg2 всё сделает за нас.
cur.execute(
    "INSERT INTO test12 (num, data) VALUES (%s, %s)",
    (100, "abc'def")
)

# Выполнить команду
cur.execute("SELECT * FROM test;")
# Но как получить результат её выполнения?..

# А вот так. fetchone — «принести» одну строчку результата,
# fetchall — все строчки.
cur.fetchone()

# Завершить транзакцию
conn.commit()
# Закрыть курсор
cur.close()
# Закрыть подключение
conn.close()






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


# «спагетти-код»
# async def process_messages(messages, do_async):
#     for message in messages:
#         try:
#             user_id = message['user']['id']
#             user = db_conn.get('user', 'id=={}'.format(user_id))
#             user.messages = user.messages + '\n' + message['text']
#             user.save()
#             if do_async:
#                 await db_conn.write_async(
#                     'message',
#                     {'text': message['text'], 'user_id': message['user']['id']}
#                 )
#             else:
#                 db_conn.write(
#                     'message',
#                     {'text': message['text'], 'user_id': message['user']['id']}
#                 )
#             return 200, 'OK'
#         except DatabaseException as exc:
#             return 400, str(exc)

# # как же написать докстроку?
# @catch_db_exceptions
# async def process_messages(messages, do_async):
#     """Process each message and update them in the user info."""
#     for message in messages:
#         user = get_user(message['user']['id'])
#         update_user_messages(user, message)
#         await process_message(message, do_async)
#         return 200, 'OK


# Иногда важно описать, за что отвечают аргументы функции, или просто дать читателю больше контекста, и в таком случае
# докстроки можно разнести на несколько строк. На строчке с первыми кавычками при этом необходимо оставить краткую
# справку о функции:
# @catch_db_exceptions
# async def process_messages(messages, do_async):
#     """Process each message and update them in the user info.
#
#     You can use this function as a shortcut when you don't care
#     about manually specifying parameters for the update and just
#     want control over whether or not messages will be processed
#     synchronously.
#
#     Parameters
#         ----------
#         messages : list[Message]
#             List of messages
#         do_async : bool
#             Whether to run the processing asynchronously
#     """
#     for message in messages:
#         user = get_user(message['user']['id'])
#         update_user_messages(user, message)
#         await process_message(message, do_async)
#         return 200, 'OK'


# # Для классов докстроки составляются аналогично: можно писать однострочные, а можно многострочные, в которых будут
# # описаны методы и переменные класса. При этом для каждого метода можно написать свою документацию:
# class DatabaseProcess:
#     """
#     A process interacting with a database
#
#     Attributes
#     ----------
#     db_name : str
#         database name
#     timeout : int
#         connection timeout (in ms)
#
#     Methods
#     -------
#     get(entity_name, id=None)
#         Gets entity by name and an optional ID.
#     """
#
#     db_name = "users"
#
#     def get(self, entity_name, entity_id=None):
#         """Gets entity by name and an optional ID.
#
#         If the argument `entity_id` isn't passed in,
#         the first entity is returned.
#
#         Parameters
#         ----------
#         entity_name: str
#             The entity name (also known as the table name).
#         entity_id : int, optional
#             The ID of the entity.
#
#         Raises
#         ------
#         DatabaseError
#             If the database returned an error.
#         """
#
#         return db_conn.get(
#             table=entity_name,
#             filters=(
#                 {'id': entity_id}
#                 if entity_id is not None
#                 else {}
#             )
#         )


