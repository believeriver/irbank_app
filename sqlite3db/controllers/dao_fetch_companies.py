import sys
import os
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_PATH)

from sqlite3db.controllers.dao_sqlite3 import DaoSQLite3


class Companies(DaoSQLite3):

    @staticmethod
    def _set_sql_all() -> str:
        # select companies whose dividend rate is over 3%.
        dividend_rate = 3
        sql = f' select company_code, ' \
              f'company_name, ' \
              f'company_stock, ' \
              f'company_dividend, ' \
              f'company_dividend_rank, ' \
              f'company_dividend_update ' \
              f'from companies ' \
              f'where company_dividend > {float(dividend_rate)} order by company_dividend_rank;'
        return sql

    def _select_all(self):
        sql = self._set_sql_all()
        if self._conn is None:
            self._conn_db()
        return self._curs.execute(sql)

    def companies_dataset(self) -> pd.DataFrame:
        result = self._select_all()
        dataset = []
        for row in result:
            d_row = {
                '企業コード': str(row[0]),
                '企業名': row[1],
                '株価(円)': row[2],
                '配当率(%)': row[3],
                '配当ランキング': row[4],
                '更新日': row[5],
            }
            dataset.append(d_row)
        _df = pd.DataFrame(dataset)
        return _df


class FetchCompany(DaoSQLite3):

    @staticmethod
    def _set_sql_company() -> str:
        sql = f' select company_code, ' \
              f'company_name, ' \
              f'company_stock, ' \
              f'company_dividend, ' \
              f'company_dividend_rank, ' \
              f'company_dividend_update ' \
              f'from companies ' \
              f'where company_code = ?;'
        return sql

    def _select_company(self, _company_code):
        sql = self._set_sql_company()
        if self._conn is None:
            self._conn_db()
        # return self._curs.execute(sql, (company_data, company_data))
        return self._curs.execute(sql, (_company_code,))

    def fetch_company_dataset(self, _company) -> pd.DataFrame:
        result = self._select_company(_company)
        dataset = []
        for row in result:
            d_row = {
                '企業コード': str(row[0]),
                '企業名': row[1],
                '株価(円)': row[2],
                '配当率(%)': row[3],
                '配当ランキング': row[4],
                '更新日': row[5],
            }
            dataset.append(d_row)
        _df = pd.DataFrame(dataset)
        return _df


class SearchCompanyCode(DaoSQLite3):

    @staticmethod
    def _set_sql_company() -> str:
        sql = f" select company_code, " \
              f"company_name " \
              f"from companies " \
              f"where company_name like ?;"
        return sql

    def _select_company(self, _company_name):
        sql = self._set_sql_company()
        if self._conn is None:
            self._conn_db()
        logging.info({'action': 'SearchCompanyCode', 'company_name': _company_name})
        return self._curs.execute(sql, ('%'+_company_name+'%',))

    def fetch_company_dataset(self, _company) -> pd.DataFrame:
        result = self._select_company(_company)
        dataset = []
        for row in result:
            d_row = {
                '企業コード': str(row[0]),
                '企業名': row[1],
            }
            dataset.append(d_row)
        _df = pd.DataFrame(dataset)
        return _df


if __name__ == '__main__':
    companies_dataset = Companies()
    df = companies_dataset.companies_dataset()
    print('df', df)

    company_dataset = FetchCompany()
    df2 = company_dataset.fetch_company_dataset(7220)
    print('df2', df2)

    del df, df2, companies_dataset, company_dataset

