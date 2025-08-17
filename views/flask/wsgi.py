import sys
import os
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.flask_webserver import server
import config.settings

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("running server")
    server.start(config.settings.DEBUG)
