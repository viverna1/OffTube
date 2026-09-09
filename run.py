# run.py
import logging

from app import create_app
from app.shared import logger


if __name__ == '__main__':
    logger.setup_logging(logging.DEBUG)

    app = create_app()
    # app.run(host='0.0.0.0', port=5000, debug=True) 
    app.run(debug=True) 
