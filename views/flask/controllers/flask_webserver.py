from flask import Flask, redirect, render_template, request, url_for
import sys
import os
import datetime
import threading
import logging

PROJECT_PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(PROJECT_PATH)
print(PROJECT_PATH)


from sqlite3db.controllers.dao_fetch_japanstock import IRBankDB, fetch_stock_price_form_yfinance_api
from scraping.models.companies import Company
import config.settings
from views.flask.controllers.lib.utils_graph import create_ir_graph_list_df, create_stock_graph
from flask_caching import Cache


logging.basicConfig(level=logging.DEBUG,
                    format='%(threadName)s: %(message)s')


app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')
cache = Cache(app)

app.config['CACHE_TYPE'] = 'simple'  # シンプルなメモリキャッシュを使用
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # キャッシュの有効期限を300秒に設定


class WebServer(object):
    def start(self, debug=False):
        port = config.settings.PORT
        app.run(host="localhost", port=port, debug=debug)


server = WebServer()


SYSTEM_NAME = 'NONOKO'
MAX_NUM_RANKING_LIST = 1500
NUM_OF_THREAD = 2


# 関数：外部APIからデータを取得する
def get_data_from_external_api(semaphore, _company_code, label, dataset):
    # print(_company_code, label)
    with semaphore:
        try:
            dataset[label] = fetch_stock_price_form_yfinance_api(
                _company_code, start='2010-01-01', end=datetime.date.today(), span=30)
        except Exception as e:
            dataset[label] = []
            print({'[error]get_data_from_external_api': e})
        print({'message': 'Data from external API'})


# 関数：ローカルデータベースからデータを取得する
def get_data_from_local_database(semaphore, _company_code, label, dataset):
    # print(_company_code, label)
    _ir_bank_db = IRBankDB()
    with semaphore:
        try:
            dataset[label] = _ir_bank_db.fetch_company_ir_dataset(_company_code)
        except Exception as e:
            dataset[label] = []
            print({'[error]get_data_from_local_database': e})
        print({'message': 'Data from local database'})


@app.route("/about", methods=["GET", "POST"])
def about() -> str:
    return render_template('pages/about.html')


@app.route("/me", methods=["GET", "POST"])
def me() -> str:
    return render_template('pages/me.html')


@app.route("/", methods=["GET", "POST"])
@cache.cached(timeout=60)  # キャッシュの有効期限を60秒に設定
def hello() -> str:
    company_code_select = request.args.get("company_code_select")
    # print(company_code_select)
    companies_data = []
    if company_code_select is None:
        dao_data = Company.fetch_code_and_name()
    else:
        dao_data = Company.fetch_code_and_name_one(company_code_select)

    # print(dao_data)
    for d in dao_data:
        companies_data.append({
            1: d['company_code'],
            2: d['company_name'],
            3: d['company_stock'],
            4: d['company_dividend'],
            5: d['dividend_rank'],
            6: d['update_date']})

    if request.method == "POST":
        company_code = request.form.get("company_code")
        _company = Company.fetch_code_and_name_one(company_code)
        company_name = _company[0]['company_name']
        # print('company_name', company_name)

        if company_code != "" and len(company_code) == 4:
            company_code = company_code.strip()

            dataset = dict()
            semaphore = threading.Semaphore(NUM_OF_THREAD)
            thread1 = threading.Thread(target=get_data_from_external_api,
                                       args=(semaphore, company_code, 'yfinance', dataset))
            thread2 = threading.Thread(target=get_data_from_local_database,
                                       args=(semaphore, company_code, 'ir_bank', dataset))
            thread1.start()
            thread2.start()
            thread1.join()
            thread2.join()
            # print({'dataset by threading': dataset})
            datasets, stock_datasets = dataset['ir_bank'], dataset['yfinance']

            if datasets is not None:
                # temp = datasets
                temp = datasets.copy()
                # print({'temp': temp})
                try:
                    graph_stock = create_stock_graph(stock_datasets, title=str(company_name) + ' 株価')
                except Exception as e:
                    graph_stock = []
                    print({'graph_stock': e})

                try:
                    graph_ir_list, copy_data = create_ir_graph_list_df(temp)
                except Exception as e:
                    graph_ir_list, copy_data = [], []
                    print({'graph_ir_list': e})

                return render_template(
                    "pages/dashboard_detail.html", company_code=company_code,
                    company_name=company_name, datasets=copy_data,
                    graph_stock=graph_stock, graph_ir_list=graph_ir_list)
            else:
                print('no data')
        else:
            redirect('/')
    # GETの処理（ホームのページ）
    return render_template("pages/dashboard_index.html",
                           name=SYSTEM_NAME,
                           companies_data=companies_data[0:MAX_NUM_RANKING_LIST])