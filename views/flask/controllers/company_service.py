import sys
import os
import threading
import logging
import datetime


PROJECT_PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(PROJECT_PATH)
# print(PROJECT_PATH)

from models.fetch_japnese_stock_from_finence_api import fetch_stock_dataframe
from models.fetch_company_info_from_database import DataAccessObject

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.propagate = False
logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


class CompanyService(object):
    def __init__(self, company_code=None):
        self.company_code = company_code
        self.dao = DataAccessObject()

    def fetch_company_list(self, code=None):
        if code:
            companies = self.dao.fetch_company_info_by_code(code)
        else:
            companies = self.dao.fetch_companies_info()
        return self._format_companies_data(companies)

    @staticmethod
    def _format_companies_data(_data):
        companies_data = []
        for d in _data:
            companies_data.append({
                1: d['company_code'],
                2: d['company_name'],
                3: d['industry'],
                4: d['description'],
                5: d['company_dividend'],
                6: d['dividend_rank'],
                7: d['company_stock'],
                8: d['per'],
                9: d['pbr'],
                10: d['update_date']})
        return companies_data

    def fetch_external_api_data(self):
        try:
            return fetch_stock_dataframe(
                self.company_code,
                start='2010-01-01',
                end=datetime.date.today(),
                span=30)
        except Exception as e:
            logger.error(f"External api data error: {e}")
            return []

    def fetch_local_data(self):
        try:
            return self.dao.fetch_financials_dataframe_by_code(
                self.company_code)
        except Exception as e:
            logger.error(f"Local data error: {e}")
            return []

    def fetch_all_data(self):
        dataset = dict()

        def f_ext():
            dataset['stock'] = self.fetch_external_api_data()

        def f_loc():
            dataset['ir_bank'] = self.fetch_local_data()

        threads = [threading.Thread(target=f_ext), threading.Thread(target=f_loc)]
        for t in threads: t.start()
        for t in threads: t.join()
        return dataset
