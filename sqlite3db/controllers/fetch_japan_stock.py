import logging
import sys
import gc
import os
import pandas as pd

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_PATH)

import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import yfinance as yf
import datetime

# logging.basicConfig(level=logging.INFO, stream=sys.stdout)
# logger = logging.getLogger(__name__)


class JapanStockModel(object):
    def __init__(self, _ticker_symbol, _start, _end=datetime.date.today()):
        self.train = None
        self.ticker_symbol = _ticker_symbol
        self.start = _start
        self.end = _end
        self._duration = 30

    @staticmethod
    def fetch_japan_stock(_ticker_symbol: int,
                          _start: str, _end) -> pd.DataFrame:
        ticker_symbol_dr = str(_ticker_symbol) + ".T"
        # end = datetime.date.today()
        end = _end
        yf.pdr_override()
        _df = pdr.get_data_yahoo(ticker_symbol_dr, _start, end)
        _df.insert(0, "code", _ticker_symbol, allow_duplicates=False)
        return _df

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    def import_data(self):
        # self.train, self.test, self.sample = self._import_csv()
        self.train = self.fetch_japan_stock(self.ticker_symbol, self.start, self.end)

    def plot_stock(self):
        self.train['Close'].plot(figsize=(12, 6), color='green')
        plt.show()


"""
Test this clas.

fetch GMO stock and plot graph.
"""


def test_main_no_prediction():
    ticker_symbols = {'GMO': 7177,
                      'JapanCeramic': 6929,
                      'MHI': 7011,
                      'Zaoh': 9986,
                      'mirai': 7931}
    start = '1990-01-01'
    end = datetime.date.today()
    span = 365

    machin_learning = JapanStockModel(ticker_symbols['MHI'], start, end)
    machin_learning.duration = span
    machin_learning.import_data()
    machin_learning.plot_stock()


if __name__ == '__main__':
    test_main_no_prediction()

    gc.collect()
    logging.info({'action': 'garbage collection', 'gc': gc.get_stats()[2]})
