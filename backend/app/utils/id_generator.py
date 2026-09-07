# id_generator.py
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