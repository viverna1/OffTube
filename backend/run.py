from app import create_app
from app.core import logger


if __name__ == '__main__':
    logger.setup_logging()

    app = create_app()
    app.run(debug=False) 
