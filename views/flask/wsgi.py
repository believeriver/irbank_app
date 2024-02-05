import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from app.controllers.flask_webserver import app
from controllers.flask_webserver import app
application = app

if __name__ == "__main__":
    application.run()
