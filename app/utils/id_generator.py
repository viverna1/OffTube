# id_generator.py

import uuid

# ? Могу предложить такой вариант.
# ? Он возвращает строку вида "6c84fb90-12c4-11e1-840d-7b25c5ee775a"
def generate_id() -> str:
    return str(uuid.uuid4())
# я думаю это излишне
# мь
# ладно
# ? это проще, быстрее и надежнее
# ? Тебе не нравится длина?
# не знаю

# ? просто я не вижу смысла думать о длине, внешнем виде и прочем
# ? типо оно вот вообще мало на что влияет
# ? ну и к слову, вся база данных 1с
# ? а это порядка 300 тысяч документов держаться на таком ID
# ? но я не заставляю


_current_id = 0

def next_id() -> str:
    global _current_id
    _current_id += 1
    return str(_current_id)

def reset_id():
    global _current_id
    _current_id = 0


# class Id:
#     _current_id = 0

#     @classmethod
#     def next_id(cls) -> str:
#         cls._current_id += 1
#         return str(cls._current_id)

#     @classmethod
#     def reset(cls):
#         cls._current_id = 0

# next_id = Id.next_id
# reset = Id.reset