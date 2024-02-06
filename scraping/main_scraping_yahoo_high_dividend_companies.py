import gc
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# print(os.path.dirname(os.path.abspath(__file__)))

from controllers.scraping_url_yahoofinace import CompanyData, FetchDataFromYahooFinance
from models.companies import Company


def fetch_index_date(c_list: CompanyData):
    fetch_yahoo = FetchDataFromYahooFinance(1, c_list)
    max_idx, update_day = fetch_yahoo.fetch_max_page_index()
    update_day = update_day.split('(')[1]
    update_day = update_day.strip(')')
    # print(max_index, update_date)
    return max_idx, update_day


if __name__ == '__main__':
    debug_flg = True

    company_list = CompanyData()
    start_index = 1
    max_index, update_date = fetch_index_date(company_list)
    print(max_index, update_date)

    if debug_flg:
        max_index = 1

    for i in range(start_index, max_index+1):
        print('page=', i)
        fetch_yahoo_finance = FetchDataFromYahooFinance(i, company_list)
        fetch_yahoo_finance.update_date = update_date
        fetch_yahoo_finance.fetch_main_soup(delay=3)
        fetch_yahoo_finance.fetch_select_item()

        # print(company_list.companies)
        # write DB
        for company in company_list.companies:
            c_code = company['company_code']
            c_name = company['company_name']
            c_stock = company['company_stock']
            c_dividend = company['company_dividend']
            c_rank = company['company_rank']
            c_date = company['company_rank_date']

            if debug_flg:
                print(c_code, c_name)

            company = Company.get_or_create(
                int(c_code), c_name, c_stock, float(c_dividend), int(c_rank), str(c_date)
            )

    gc.collect()



