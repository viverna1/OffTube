# utils.py

def formate_time(time: float):
    hours = int(time // 3600)
    minutes = int((time % 3600) // 60)
    seconds = int(time % 60)

    if hours > 0:
        return f"{hours:2d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:2d}:{seconds:02d}"

class IdGenerator:
    current_id = 0

    @classmethod
    def get_id(cls) -> str:
        cls.current_id += 1
        return str(cls.current_id)
    