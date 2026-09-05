# logger.py
import logging

IMPORTANT = 25


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
    IMPORTANT: COLORS.YELLOW,
    logging.WARNING: COLORS.YELLOW,
    logging.ERROR: COLORS.RED,
    logging.CRITICAL: COLORS.MAGENTA,
}


class CustomLogger(logging.Logger):
    def important(self, message: object, *args, **kwargs, ) -> None:
        if self.isEnabledFor(IMPORTANT):
            self._log(IMPORTANT, message, args, **kwargs)

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

    # Фильтр для логов Flask
    logging.getLogger('werkzeug').addFilter(StaticFilter())

    # Кастомный уровень логирования "IMPORTANT"
    logging.setLoggerClass(CustomLogger)
    logging.addLevelName(IMPORTANT, "IMPORTANT")


if __name__ == "__main__":
    setup_logging()
    log = logging.getLogger(__name__)
    log.debug("Debug message")
    log.info("Info message")
    log.warning("Warning message")
    log.error("Error message")
    log.critical("Critical message")
    log.important("Important message")  # Custom level
    try:
        x = 1 / 0
    except Exception as e:
        log.exception("Exception:")