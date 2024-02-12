import sys
import os
import datetime
import logging
import pandas as pd
import numpy as np

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_PATH)
# print({'dao_fetch_japanstock.py': PROJECT_PATH})

from sqlite3db.controllers.dao_sqlite3 import DaoSQLite3
from sqlite3db.controllers.fetch_japan_stock import JapanStockModel

# logging.basicConfig(level=logging.INFO, stream=sys.stdout)
# logger = logging.getLogger(__name__)


def fetch_stock_price_form_yfinance_api(company_code, start='2010-01-01', end=datetime.date.today(), span=30):
    if company_code is None:
        return None

    dataset = JapanStockModel(company_code, start, end)
    dataset.duration = span
    dataset.import_data()
    d_year = dataset.train.index
    data = np.array(dataset.train['Close'])
    d = {'year': d_year,
         'value': data}
    df = pd.DataFrame(d)
    del dataset

    return df


class IRBankDB(DaoSQLite3):

    @staticmethod
    def set_sql() -> str:
        sql = 'SELECT cp.company_name AS "企業名",' \
                   'sa.year AS "年",' \
                   'sa.amount_sales AS "売上高",' \
                   'om.margin AS "営業利益率",' \
                   'e.eps AS "EPS",' \
                   'ca.ratio AS "自己資本比率",' \
                   'cf.cash AS "営業活動によるCF",' \
                   'ce.cash AS "現金等",' \
                   'cd.cash AS "一株配当",' \
                   'dr.ratio AS "配当性向"' \
                   'FROM eps AS e ' \
                   'LEFT OUTER JOIN operating_margins AS om ' \
                   'ON (e.year = om.year) and (e.company_code = om.company_code)' \
                   'LEFT OUTER JOIN sales as sa ON (sa.year = e.year) and (sa.company_code = e.company_code)' \
                   'LEFT OUTER JOIN capital_adequacy as ca ' \
                   'ON (sa.year = ca.year) and (e.company_code = ca.company_code)' \
                   'LEFT OUTER JOIN cash_flows as cf ON (e.year = cf.year) and (e.company_code = cf.company_code)' \
                   'LEFT OUTER JOIN cash_equivalents as ce ' \
                   'ON (e.year = ce.year) and (e.company_code = ce.company_code)' \
                   'LEFT OUTER JOIN cash_dividends as cd ON (e.year = cd.year) and (e.company_code = cd.company_code)' \
                   'LEFT OUTER JOIN dividend_ratio as dr ON (e.year = dr.year) and (e.company_code = dr.company_code)' \
                   'LEFT OUTER JOIN companies as cp ON (e.company_code = cp.company_code)' \
                   'WHERE e.company_code = ?;'
        return sql

    def _select_all_irdata(self, _company_code):
        sql = self.set_sql()
        if self._conn is None:
            self._conn_db()
        return self._curs.execute(sql, (_company_code,))

    def fetch_company_ir_dataset_direct_sql(self, company_code):
        return self._select_all_irdata(company_code)

    def fetch_company_ir_dataset(self, company_code) -> pd.DataFrame:
        result = self._select_all_irdata(company_code)
        dataset = []
        for row in result:
            d_row = {
                '企業名': row[0],
                '年': row[1],
                '売上高(円)': int(row[2]),
                '営業利益率(%)': float(row[3]),
                'EPS': float(row[4]),
                '自己資本率(%)': row[5],
                '営業活動によるCF(円)': row[6],
                '現金等(円)': row[7],
                '一株配当(円)': row[8],
                '配当性向(%)': row[9],
            }
            dataset.append(d_row)
        _df = pd.DataFrame(dataset)
        return _df

    @staticmethod
    def fetch_stock_price_data(company_code, start='2010-01-01', end=datetime.date.today(), span=30):
        if company_code is None:
            return None

        dataset = JapanStockModel(company_code, start, end)
        dataset.duration = span
        dataset.import_data()
        d_year = dataset.train.index
        data = np.array(dataset.train['Close'])
        d = {'year': d_year,
             'value': data}
        df = pd.DataFrame(d)
        del dataset

        return df


"""
Test this clas.

fetch stock(9986) from database.
"""


def test_main():
    db = IRBankDB()

    print('--- irbank dataset ---')
    df = db.fetch_company_ir_dataset(9986)
    print(df)

    print('--- stock price from yfinance ---')
    df_stock = db.fetch_stock_price_data(9986)
    print(df_stock)


if __name__ == '__main__':
    test_main()
