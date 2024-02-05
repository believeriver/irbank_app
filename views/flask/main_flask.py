import logging
import sys
import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_PATH)
print(PROJECT_PATH)

from controllers.flask_webserver import server
import config.settings

logging.basicConfig(filename=config.settings.LOG_FILE, level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.info("running server")
    server.start(config.settings.DEBUG)
