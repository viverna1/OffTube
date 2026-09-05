# id_generator.py

class IdGenerator:
    current_id = 0

    @classmethod
    def get_id(cls) -> str:
        cls.current_id += 1
        return str(cls.current_id)