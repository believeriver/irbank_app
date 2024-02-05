import os
import sys

PROJECT_PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_PATH)
# print(PROJECT_PATH)

from views.streamlit import start_streamlit_db


if __name__ == '__main__':
    start_streamlit_db()
