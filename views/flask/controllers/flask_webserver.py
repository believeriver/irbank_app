import sys
import os
import logging

from flask import Flask, redirect, render_template, request, url_for
from flask_caching import Cache

PROJECT_PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(PROJECT_PATH)

import config.settings
from views.flask.controllers.utils_graph import create_ir_graph_list_df, create_stock_graph
from views.flask.controllers.company_service import CompanyService

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

SYSTEM_NAME = 'NONOKO'
MAX_NUM_RANKING_LIST = 1500


class WebServer(object):
    def __init__(self):
        self.app = Flask(__name__,
                         template_folder='../templates',
                         static_folder='../static')
        self.app.config['CACHE_TYPE'] = 'simple'
        self.app.config['CACHE_DEFAULT_TIMEOUT'] = 300
        self.cache = Cache(self.app)
        self._add_routes()

    def _add_routes(self):
        self.app.add_url_rule("/about", "about", self.about)
        self.app.add_url_rule("/me", "me", self.me)
        self.app.add_url_rule(
            "/", "financial_information",
            self.financial_information,
            methods=["GET", "POST"])

    @staticmethod
    def about():
        return render_template('pages/about.html')

    @staticmethod
    def me():
        return render_template('pages/me.html')

    @staticmethod
    def financial_information():
        company_code_select = request.args.get("company_code_select")
        service = CompanyService()
        companies_data = service.fetch_company_list(company_code_select)

        if request.method == "POST":
            company_code = request.form.get("company_code", '').strip()
            logger.info({"company_code": company_code})
            if not (company_code and len(company_code) == 4):
                return redirect(url_for('financial_information'))
                # return redirect('/')

            detail_service = CompanyService(company_code)
            dataset = detail_service.fetch_all_data()
            ir_data = dataset.get('ir_bank')
            stock_data = dataset.get('stock')
            company_info = detail_service.dao.fetch_company_info_by_code(company_code)
            company_name = ''
            if company_info:
                company_name = company_info[0]['company_name']
                # logger.debug({'company_name': company_name})

            try:
                graph_stock = create_stock_graph(
                    stock_data, title=str(company_name) + ' 株価')
            except Exception as e:
                graph_stock = []
                print({'graph_stock': e})

            try:
                temp = ir_data.copy()
                graph_ir_list, copy_data = create_ir_graph_list_df(temp)
            except Exception as e:
                graph_ir_list, copy_data = [], []
                print({'graph_ir_list': e})

            return render_template(
                "pages/dashboard_detail.html",
                company_code=company_code,
                company_name=company_name,
                datasets=copy_data,
                graph_stock=graph_stock,
                graph_ir_list=graph_ir_list)

        # GETの処理（ホームのページ）
        return render_template(
            "pages/dashboard_index.html",
            name=SYSTEM_NAME,
            companies_data=companies_data[0:MAX_NUM_RANKING_LIST])

    def start(self, debug=False, port=config.settings.PORT):
        self.app.run(host="localhost", port=port, debug=debug)


# Create WebServer
server = WebServer()
