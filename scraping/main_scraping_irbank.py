import gc
from typing import List
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# print(os.path.dirname(os.path.abspath(__file__)))

from controllers.scraping_url_irbank import CompanyData, FetchDataFromIRBank
from models.sales import Sales
from models.companies import Company
from models.operating_margins import Margins
from models.eps import EPS
from models.capital_adequacy import CapitalAdequacy
from models.cash_flow import CashFlow
from models.cash_equivalents import CashEquivalents
from models.cash_dividend import CashDividend
from models.dividend_ratio import DividendRatio


def fetch_companies_list() -> List[int]:
    result = []
    dao_data = Company.fetch_code_and_name()
    for d in dao_data:
        result.append(d['company_code'])
    return result


def to_db(c_code, tb_name, tr_data):
    for data in tr_data:
        c_year, c_data = data[0], data[1]
        print(tb_name, c_year, c_data)
        if tb_name == "売上高":
            sales = Sales.get_or_create(
                int(c_code), c_year, c_data)
        elif tb_name == "営業利益率":
            op_margin = Margins.get_or_create(
                int(c_code), c_year, c_data)
        elif tb_name == "EPS":
            eps = EPS.get_or_create(
                int(c_code), c_year, c_data)
        elif tb_name == "自己資本比率":
            capital_adequacy = CapitalAdequacy.get_or_create(
                int(c_code), c_year, c_data)
        elif tb_name == "営業活動によるCF":
            cash_flow = CashFlow.get_or_create(
                int(c_code), c_year, c_data)
        elif tb_name == "現金等":
            cash_equivalents = CashEquivalents.get_or_create(
                int(c_code), c_year, c_data)
        elif tb_name == "一株配当":
            if c_data == '-':
                c_data = 0
            cash_dividend = CashDividend.get_or_create(
                int(c_code), c_year, c_data)
        elif tb_name == "配当性向":
            if c_data == '-':
                c_data = 0
            dividend_ratio = DividendRatio.get_or_create(
                int(c_code), c_year, c_data)


def table_item_list() -> List[str]:
    items = [
        "売上高",
        "営業利益率",
        "EPS",
        "自己資本比率",
        "営業活動によるCF",
        "現金等",
        "一株配当",
        "配当性向"]
    return items


def main_check_companies_list(debug_flg=False):
    dao_company_list = fetch_companies_list()
    if debug_flg:
        print({'companies_list': dao_company_list})


def main_ir_scraping(debug_flg=False):

    dao_company_list = fetch_companies_list()

    if debug_flg:
        company_code_list = [9986, 9110]
    else:
        company_code_list = dao_company_list[1001:1002]

    table_items = table_item_list()

    # fetch companies dataset
    for index, company_code in enumerate(company_code_list):
        # scraping
        company_datasets = CompanyData()
        fetch_ir_bank = FetchDataFromIRBank(company_datasets, company_code)
        fetch_ir_bank.fetch_main_soup(delay=1)

        for table_item in table_items:
            if debug_flg:
                # table_item = table_items[1]
                print(company_code, table_item)
            fetch_ir_bank.fetch_table_data(table_item)

        # write database
        for company in company_datasets.companies:
            c_name = company['company_name']
            c_code = company['company_code']
            tb_name = company['item_name']
            tr_data = company['trend_data']
            print('write database -> ', c_name, tb_name, '---')
            to_db(c_code, tb_name, tr_data)

            # test write csv
            # fetch_IR_bank.test_to_csv(c_code, tb_name)

        if debug_flg:
            print(index, 'delete object')

        del company_datasets, fetch_ir_bank

    gc.collect()


if __name__ == '__main__':
    debug = False
    main_check_companies_list(debug)
    main_ir_scraping(debug)



