import os
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

path_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
USER_AGENT = '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0'

# DB_PATH = path_dir + '/irbank/db/'
DB_PATH = path_dir + '/irbank/sqlite3db/'
LOG_FILE = 'appserver.log'
PORT = 8000
# DEBUG = True
DEBUG = False

if DEBUG:
    DB_NAME = DB_PATH + 'test.sql'
    logger.info({'action': 'settings.py', 'path_dir': DB_NAME})
else:
    DB_NAME = DB_PATH + 'IRBank_database.sql'

