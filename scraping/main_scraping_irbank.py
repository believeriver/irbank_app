import gc
from typing import List
import sys
import os
import logging
from optparse import OptionParser
from itertools import chain

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# print(os.path.dirname(os.path.abspath(__file__)))

from controllers.scraping_url_irbank import CompanyData, FetchDataFromIRBank
from models.companies import Company
from models.financial_data import Financial
# import utils  # -> include: Company, Financial data model


handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.propagate = False
logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


class ScrapingIRBank(object):
    def __init__(self, _start: int, _end: int):
        self.start_index = _start
        self.end_index = _end
        self.dao_company_list = self.fetch_companies_list()
        self.company_code_list = self.dao_company_list[_start:_end]
        self.table_items = self.table_item_list()

    @staticmethod
    def fetch_companies_sorted_by_rank():
        company_list = Company.fetch_code_and_name()
        sorted_ranking = sorted(company_list, key=lambda x: x["dividend_rank"])
        return sorted_ranking

    def fetch_companies_list(self) -> List[int]:
        result = []
        # dao_data = Company.fetch_code_and_name()
        dao_data = self.fetch_companies_sorted_by_rank()
        for d in dao_data:
            result.append(d['company_code'])
        return result

    @staticmethod
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

    @staticmethod
    def fetch_financial_datasets(company_datasets: CompanyData):
        results = []
        for company in company_datasets.companies:
            c_name = company['company_name']
            c_code = company['company_code']
            tb_name = company['item_name']
            tr_data = company['trend_data']
            logger.debug({
                "c_name": c_name,
                "c_code": c_code,
                "tb_name": tb_name,
            })
            trend_datasets = []
            for item in tr_data:
                if len(item) == 2:
                    logger.debug({
                        "c_code": c_code,
                        "table_name": tb_name,
                        "fiscal_year": item[0],
                        "value": item[1]
                    })
                    temp = [c_code, tb_name, item[0][0:4], item[1]]
                    trend_datasets.append(temp)
            if not trend_datasets:
                trend_datasets.append([c_code, tb_name, None, None])
            results.append(trend_datasets)
        return results

    @staticmethod
    def marge_financial_datasets(_datasets):
        data = list(chain.from_iterable(_datasets))
        temp_dict = {}
        for c_code, item, fiscal_year, value in data:
            key = (c_code, fiscal_year)
            if key[1] is not None:
                if key not in temp_dict:
                    # c_code と fiscal_year を保持し、項目は空辞書で初期化
                    temp_dict[key] = {"company_code": c_code, "fiscal_year": fiscal_year}
                # 該当項目名で値をセット
                temp_dict[key][item] = value

        # 辞書のリストに変換
        result_list = list(temp_dict.values())
        return result_list

    def save_to_financial_database(self, _dataset):
        code = _dataset.get("company_code", None)
        fiscal_year = _dataset.get("fiscal_year", None)
        sale = _dataset.get(self.table_items[0], None)
        margin = _dataset.get(self.table_items[1], None)
        eps = _dataset.get(self.table_items[2], None)
        equity = _dataset.get(self.table_items[3], None)
        cashflow = _dataset.get(self.table_items[4], None)
        equivalents = _dataset.get(self.table_items[5], None)
        dividend = _dataset.get(self.table_items[6], None)
        payout = _dataset.get(self.table_items[7], None)

        db_financial = Financial.get_or_create(
            code, fiscal_year, sale, margin, eps, equity,
            cashflow, equivalents, dividend, payout)
        logger.info({
            "action": "save_financial_database",
            "company_code": db_financial.company_code,
            "fiscal_year": db_financial.fiscal_year,
        })

    def start(self):
        # fetch companies dataset
        for index, company_code in enumerate(self.company_code_list):
            # scraping
            logger.info({"index": index, "code": company_code})
            company_datasets = CompanyData()
            fetch_ir_bank = FetchDataFromIRBank(
                company_datasets, company_code)
            fetch_ir_bank.fetch_main_soup(delay=1)

            for table_item in self.table_items:
                logger.debug({
                    "company_code": company_code,
                    "table": table_item,
                })
                fetch_ir_bank.fetch_table_data(table_item)

            # write database
            financial_datasets = self.fetch_financial_datasets(company_datasets)
            dao_datasets = self.marge_financial_datasets(financial_datasets)

            for record in dao_datasets:
                logger.debug(record)
                self.save_to_financial_database(record)

            del company_datasets, fetch_ir_bank, financial_datasets, dao_datasets

        gc.collect()


def main():
    usage = 'usage: %prog -s <start index> -e <end index>'
    parser = OptionParser(usage=usage)
    parser.add_option('-s', '--start', action='store', type='int', dest='start', help='start index')
    parser.add_option('-e', '--end', action='store', type='int', dest='end', help='end index')
    options, args = parser.parse_args()

    start_index = int(options.start)
    end_index = int(options.end)
    logger.info({
        'start': start_index,
        'end': end_index,
    })

    if start_index is None or end_index is None:
        raise Exception("start and end index are required.")

    scraping = ScrapingIRBank(start_index, end_index)
    scraping.start()

    gc.collect()


if __name__ == '__main__':
    # max index : 3372
    main()







