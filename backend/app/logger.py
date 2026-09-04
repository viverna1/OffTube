# logger.py
import logging

class COLORS:
    RESET = '\033[0m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'

LEVEL_COLORS = {
    logging.DEBUG: COLORS.CYAN,
    logging.INFO: COLORS.GREEN,
    logging.WARNING: COLORS.YELLOW,
    logging.ERROR: COLORS.RED,
    logging.CRITICAL: COLORS.MAGENTA,
}


class CustomFormatter(logging.Formatter):
    def format(self, record):
        color = LEVEL_COLORS.get(record.levelno, '')
        record.levelname = f"{color}{record.levelname}{COLORS.RESET}"
        return super().format(record)


# фильтр для исключения лишних логов Flask
class StaticFilter(logging.Filter):
    def filter(self, record):
        return ('/static/' not in record.getMessage()
                and "/thumbnails/" not in record.getMessage() 
                and "/thumbnail" not in record.getMessage() 
                and "/duration" not in record.getMessage()
                )


def setup_logging():
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    format='%(name)s [%(levelname)s] %(funcName)s: %(message)s'
    handler.setFormatter(CustomFormatter(format))

    logging.basicConfig(level=logging.DEBUG, handlers=[handler])

    logging.getLogger('werkzeug').addFilter(StaticFilter())