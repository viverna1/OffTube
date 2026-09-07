# logger.py
import logging

FLASK = 19

class COLORS:
    RESET = '\033[0m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    PURPLE = '\033[38;5;63m'
    BOLD = '\033[1m'


LEVEL_COLORS = {
    logging.DEBUG: COLORS.CYAN,
    logging.INFO: COLORS.GREEN,
    logging.WARNING: COLORS.YELLOW,
    logging.ERROR: COLORS.RED,
    logging.CRITICAL: COLORS.BOLD + COLORS.RED,
    FLASK: COLORS.PURPLE
}



class CustomFormatter(logging.Formatter):
    def format(self, record):
        if record.name == "werkzeug" and record.levelno == logging.INFO:
            record.levelname = "FLASK"
            record.levelno = FLASK
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


def setup_logging(level=logging.DEBUG):
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    format='%(filename)s:%(lineno)s [%(levelname)s]: %(message)s'
    handler.setFormatter(CustomFormatter(format))

    logging.basicConfig(level=level, handlers=[handler])

    # Фильтр для логов Flask
    logging.getLogger('werkzeug').addFilter(StaticFilter())


if __name__ == "__main__":
    setup_logging()
    log = logging.getLogger(__name__)
    log.debug("Debug message")
    log.info("Info message")
    log.warning("Warning message")
    log.error("Error message")
    log.critical("Critical message")
    try:
        x = 1 / 0
    except Exception as e:
        log.exception("Exception:")