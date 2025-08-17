import sys
import os
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.flask_webserver import server

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

application = server.app


if __name__ == "__main__":
    logger.info("running server")
    application.run(debug=False, threaded=True)
