import sys
import os
import logging
import pandas as pd
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraping.models.query_company_financials import CompanyInformation, Company, Financial

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)
logger.propagate = False
logger.addHandler(handler)


class DataAccessObject(object):
    def __init__(self):
        self.company_obj = Company()
        self.financial_obj = Financial()
        self.company_info_obj = CompanyInformation()

    def fetch_companies_sorted_by_rank(self):
        company_list = self.company_obj.fetch_code_and_name()
        sorted_ranking = sorted(company_list, key=lambda x: x["dividend_rank"])
        return sorted_ranking

    def fetch_company_by_code(self, _company_code):
        return self.company_obj.fetch_code_and_name_one(_company_code)

    def fetch_company_info_by_code(self, _company_code):
        return self.company_info_obj.get_information_by_code(_company_code)

    def fetch_companies_info(self):
        company_info = self.company_info_obj.get_information_by_code()
        sorted_info = sorted(company_info, key=lambda x: x["dividend_rank"])
        return sorted_info

    def fetch_financials_by_code(self, _company_code):
        financials = self.financial_obj.get_financials_by_company_code(_company_code)
        sorted_financials = sorted(financials, key=lambda x: x["fiscal_year"])
        return sorted_financials

    def fetch_financials_dataframe_by_code(self, _company_code) -> pd.DataFrame:
        rows = self.fetch_financials_by_code(_company_code)
        dataset = []
        for row in rows:
            d_row = {
                '企業名': row['company_code'],
                '年': row['fiscal_year'],
                '売上高(円)': row['sales'],
                '営業利益率(%)': row['operating_margin'],
                'EPS': row['eps'],
                '自己資本率(%)': row['equity_ratio'],
                '営業活動によるCF(円)': row['operating_cash_flow'],
                '現金等(円)': row['cash_and_equivalents'],
                '一株配当(円)': row['dividend_per_share'],
                '配当性向(%)': row['payout_ratio'],
            }
            dataset.append(d_row)
        _df = pd.DataFrame(dataset)
        return _df


def main_test1():
    dao = DataAccessObject()
    _companies = dao.fetch_companies_sorted_by_rank()
    for company in _companies[0:3]:
        rows = dao.fetch_company_info_by_code(company['company_code'])
        for row in rows:
            print(row)
        print('-'*50)

    print('*'*50)
    company_code = _companies[1]['company_code']
    rows = dao.fetch_financials_by_code(company_code)
    for row in rows:
        print(row['company_code'],
              row['fiscal_year'],
              row['sales'],
              row['operating_margin'],
              row['eps'],
              row['equity_ratio'],
              row['operating_cash_flow'],
              row['cash_and_equivalents'],
              row['dividend_per_share'],
              row['payout_ratio'],
              )


def main():
    dao = DataAccessObject()
    _companies = dao.fetch_companies_sorted_by_rank()
    company_code = _companies[1]['company_code']
    df = dao.fetch_financials_dataframe_by_code(company_code)
    print(df)

    print(dao.fetch_company_by_code(company_code))
    print(dao.fetch_company_info_by_code(company_code))
    print('-'*50)
    for item in dao.fetch_companies_info()[0:3]:
        print(item)


if __name__ == '__main__':
    main()

