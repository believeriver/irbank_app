import sys
import os
from time import sleep
import gc
from typing import Optional
from selenium.webdriver.common.by import By

sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from scraping.controllers.i_scraping import IDataSet, IFetchDataFromUrl, ISaveToFile


class CompanyData(IDataSet):
    def __init__(self):
        self.companies = []


class FetchDataFromIRBank(IFetchDataFromUrl):
    def __init__(self, dataset: CompanyData, company_code: int) -> None:
        super().__init__()
        self.base_url = 'https://irbank.net'
        self.url = self.base_url
        self.company_code = company_code
        self.dataset = dataset
        self.delay_time = 3
        self._header = None
        self._td_obb = None
        self._td_odd = None

    def _fetch_bs_url_by_selenium(self, company_code) -> Optional[str]:
        bs_url = None
        driver = self._fetch_driver_by_selenium(self.url, self.delay_time, True, False)
        sleep(1)
        search_bar = driver.find_element("name", 'query')
        sleep(1)
        search_bar.send_keys(company_code)
        sleep(1)
        search_bar.submit()
        sleep(1)
        company_page = driver.find_element(
            By.CSS_SELECTOR, 'tr.odd.weaken')
        bs_tags = company_page.find_elements(
            By.CSS_SELECTOR, 'ul.nsq > li > a')
        for tag in bs_tags:
            if tag.text == "決算":
                bs_url = tag.get_attribute('href')
        driver.quit()
        return bs_url

    def fetch_main_soup(self, delay: int = 10) -> None:
        detail_url = self._fetch_bs_url_by_selenium(self.company_code)
        if detail_url is not None:
            self._soup_main = self._fetch_soup(detail_url, delay=delay)
        else:
            print('BS URL is not found.')

    @staticmethod
    def convert_units(value: str):
        if value == '-':
            return 0

        value = value.strip('*')
        value = value.strip('%')
        value = value.strip('円')

        convert = value.maketrans(
            {'兆': '*1000000000000,',
             '億': '*100000000,',
             '万': '*10000,',
             '百': '*100,',
             '円': ''})
        sale_formula = value.translate(convert)
        # print(sale_formula)
        values = sale_formula.split(',')

        result = 0
        for val in values:
            if val != "":
                result += eval(val)

        return result

    def test_to_csv(self, company_code, item_name):
        filename = 'lib/temp/' + str(company_code) + '_' + item_name + '.csv'
        company_data = None

        for data in self.dataset.companies:
            # print(data['company_code'], company_code)
            if int(data['company_code']) == company_code:
                company_data = data['trend_data']

        if company_data:
            with open(filename, mode='w') as fp:
                fp.write(str(company_code) + ',' + item_name + '\n')
                for data in company_data:
                    fp.write(str(data[0]) + ',' + str(data[1]) + '\n')
            print('create csv')
        else:
            print('no data')

    def fetch_table_data(self, table_name: str):
        company_name_item = self._soup_main.find('div', id='container').select_one('main > div > h1 > a')
        company_code = company_name_item.text.split(' ')[0]
        company_name = company_name_item.text.split(' ')[1]
        # print(company_code, company_name)

        test_soup = self._soup_main.find_all('div', class_='mgr inline')
        result = {}

        data = []
        for idx, item in enumerate(test_soup):
            tb_titles = item.select_one("h2")
            # print(idx, tb_titles.text)
            item_title = tb_titles.text.split('#')[0]
            # print(item_title)
            if table_name == "売上高":
                table_name_list = [table_name, "収益"]
            else:
                table_name_list = [table_name]
            #  item_title == table_name:
            if item_title in table_name_list:
                # print(tb_titles.text)
                item_year = item.select("dt")
                item_dd = item.select("dd")
                item_datasets = []
                for dd in item_dd:
                    temp = dd.select_one("span.text")
                    if temp is not None:
                        item_datasets.append(temp)
                    else:
                        item_datasets.append(dd)

                for i, y in enumerate(item_year):
                    # print(i, y.text, self.convert_units(item_datasets[i].text))
                    data.append([y.text.split('\u2009')[0], self.convert_units(item_datasets[i].text)])

        result = {
            'company_code': company_code,
            'company_name': company_name,
            'item_name': table_name,
            'trend_data': data
        }
        self.dataset.companies.append(result)

    def check_fetch_table_data(self, table_name: str):
        # company code : 9110 NSユナイテッド海運
        d_items = {
            "売上高": 'c_1',
            "営業利益率": 'c_33',
            "EPS": 'c_6',
            "自己資本比率": 'c_12',
            "営業活動によるCF": 'c_17',
            "現金等": 'c_22',
            "一株配当": 'c_24',
            "配当性向": 'c_25'
        }
        print(d_items["売上高"])
        # check
        table_soup = self._soup_main.find('div', id=d_items[table_name])
        # search table title
        tb_title = table_soup.select_one("h2")
        print(tb_title.text)
        dt_year = table_soup.select("dt")
        dt_datasets = table_soup.select("span.text")
        # year
        for i, dt in enumerate(dt_year):
            print(i, dt.text, self.convert_units(dt_datasets[i].text))
        # # score
        # for i, dt in enumerate(dt_datasets):
        #     print(i, self.convert_units(dt.text))


class SaveToCsvFile(ISaveToFile):
    def __init__(self, filename: str, dataset: CompanyData):
        super().__init__(filename, dataset)


if __name__ == '__main__':
    """
    Test the program.
    """
    db_name = 'IRBank.db'
    tb_name = 'companies'
    file_name = 'IRBank.csv'

    data_items = [
        "売上高",
        "営業利益率",
        "EPS",
        "自己資本比率",
        "営業活動によるCF",
        "現金等",
        "一株配当",
        "配当性向"]

    # scraping
    company_list = CompanyData()

    # select item
    item = data_items[0]

    fetch_IR_bank = FetchDataFromIRBank(company_list, 2914)
    fetch_IR_bank.fetch_main_soup(delay=1)
    fetch_IR_bank.fetch_table_data(item)
    # print(fetch_IR_bank.dataset.companies)
    # fetch_IR_bank.check_fetch_table_data(item)

    print(company_list.companies)

    # fetch_IR_bank.test_to_csv(9986, item)
    # fetch_IR_bank.test_to_csv(9110, item)

    gc.collect()


