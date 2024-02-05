import gc
import math
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from scraping.controllers.lib.i_scraping import IDataSet, IFetchDataFromUrl, ISaveToFile


class CompanyData(IDataSet):
    def __init__(self):
        self.companies = []


class FetchDataFromYahooFinance(IFetchDataFromUrl):
    def __init__(self, page_index, dataset: CompanyData) -> None:
        super().__init__()
        self.base_url = 'https://finance.yahoo.co.jp'
        self.url = self.base_url + '/stocks/ranking/dividendYield?market=all&term=daily&page={}'.format(page_index)
        self.dataset = dataset
        self.delay_time = 3
        self.update_date = ''

    def fetch_main_soup(self, delay: int = 10) -> None:
        self._soup_main = self._fetch_soup(self.url, delay=delay, method='requests')

    def fetch_max_page_index(self):
        url = self.url.format(1)
        soup = self._fetch_soup(url, delay=10, method='requests')
        loop_index, update = None, None
        if soup:
            page_index_area = soup.find('div', id='pagertop').find_all('p')
            for i, p_tag in enumerate(page_index_area):
                if i == 0:
                    temp = p_tag.text.strip('件中')
                    temp = temp.split(' ')
                    max_page_index = int(temp[2])
                    loop_index = math.ceil(max_page_index / 50)
                else:
                    update = p_tag.text
        return loop_index, update

    def fetch_select_item(self):
        data_tables = self._soup_main.select_one('table.zvh5L2Gz').find('tbody')
        rows_table = data_tables.select('tr._1GwpkGwB')
        for index, row in enumerate(rows_table):
            rank = row.select_one('th._2mLLY-ir._2fAZnOz6').text
            name = row.select_one('td.P452zeXX').find('a').text
            code = row.select_one('li.vv_mrYM6').text
            stock = row.select_one('td.P452zeXX.i9grwWp1').select_one('span._3rXWJKZF').text
            dividend = row.select_one('td.P452zeXX.i9grwWp1._2Iu2a9lx').select_one('span._3rXWJKZF').text.strip('+')
            # print(index, rank, code, name, stock, dividend)

            d = {
                'company_code': code,
                'company_name': name,
                'company_stock': stock,
                'company_dividend': dividend,
                'company_rank': rank,
                'company_rank_date': self.update_date
            }
            self.dataset.companies.append(d)


if __name__ == '__main__':

    company_list = CompanyData()

    fetch_yahoo_finance = FetchDataFromYahooFinance(1, company_list)
    max_index, update_date = fetch_yahoo_finance.fetch_max_page_index()
    print(max_index, update_date)

    idx = max_index
    fetch_yahoo_finance = FetchDataFromYahooFinance(idx, company_list)
    fetch_yahoo_finance.update_date = update_date
    fetch_yahoo_finance.fetch_main_soup()
    fetch_yahoo_finance.fetch_select_item()
    #
    print(company_list.companies)

    gc.collect()


