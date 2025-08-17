import sys
import os
import logging
import pandas as pd
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fetch_company_info_from_database import DataAccessObject


def check_dao_companies():
    dao = DataAccessObject()
    _companies = dao.fetch_companies_sorted_by_rank()
    for company in _companies[0:9]:
        print(company)


def check_dao_company_by_code(_code):
    dao = DataAccessObject()
    company = dao.fetch_company_by_code(_code)
    print(company)


if __name__ == '__main__':
    # check_dao_companies()
    check_dao_company_by_code(9986)