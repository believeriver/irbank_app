import sys
import os
import logging
from typing import List
import gc

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.scraping_url_minkabu import CompanyData, FetchDataFromMinkabu
from models.companies import Company
from models.informations import Information


handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)
logger.propagate = False
logger.addHandler(handler)


def numeric_or_none(val):
    """
    int or float are OK. other is None
    """
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def main(_start: int = 1, _end: int = 10):
    company_code_list = []
    company_list = Company.fetch_code_and_name()
    logger.debug({'max number of companies': len(company_list)})
    for company in company_list[_start:_end]:
        logger.debug({'code': company['company_code']})
        company_code_list.append(company['company_code'])

    for index, company_code in enumerate(company_code_list):
        logging.info({"index": index, "code": company_code})
        datasets = CompanyData()
        scraping = FetchDataFromMinkabu(datasets, company_code)
        scraping.fetch_soup_main(delay=3)
        scraping.fetch_select_item()
        for company in datasets.companies:
            logging.debug(company)
            c_code = company['code']
            c_industry = company['industry']
            c_description = company['description']
            c_per = numeric_or_none(company['per'])
            c_psr = numeric_or_none(company['psr'])
            c_pbr = numeric_or_none(company['pbr'])
            db_info = Information.get_or_create(
                c_code, c_industry, c_description, c_per, c_psr, c_pbr)

            logger.info({
                "code": db_info.company_code,
                "industry": db_info.industry,
                "PER": db_info.per,
                "PSR": db_info.psr,
                "PBR": db_info.pbr,
                "updated_at": db_info.updated_at,
            })


if __name__ == '__main__':
    # max = 3372
    main(20, 25)
    # main(4, 500)
    # main(0, 9)
    # main(600, 601)

