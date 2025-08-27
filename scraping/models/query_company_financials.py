import sys
import os

from sqlalchemy import and_, or_

sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))


from scraping.models.db import BaseDatabase, database
from scraping.models.companies import Company
from scraping.models.financial_data import Financial
from scraping.models.informations import Information


class CompanyFinancial(BaseDatabase):
    __tablename__ = "company_financial"

    def get_financial_by_code(self, code):
        result = []
        rows = self._get_financials_outer_join(code)
        for row in rows:
            if row:
                result.append({
                    "company_code": row.company_code,
                    "company_name": row.company_name,
                    'industry': row.industry,
                    'description': row.description,
                    'per': row.per,
                    'psr': row.psr,
                    'pbr': row.pbr,
                    'company_stock': row.company_stock,
                    'company_dividend': row.company_dividend,
                    'dividend_rank': row.company_dividend_rank,
                    'update_date': row.company_update_date,
                    "sales": row.sales,
                    "operating_margin": row.operating_margin,
                    "eps": row.eps,
                    "equity_ratio": row.equity_ratio,
                    "operating_cash_flow": row.operating_cash_flow,
                    "cash_and_equivalents": row.cash_and_equivalents,
                    "dividend_per_share": row.dividend_per_share,
                    "payout_ratio": row.payout_ratio,
                    "fiscal_year": row.fiscal_year,
                })
        return result

    @staticmethod
    def _get_financials_outer_join(_target_code):
        _session = database.connect_db()
        query = (
            _session.query(
                Company.company_code.label("company_code"),
                Company.company_name.label("company_name"),
                Information.industry.label("industry"),
                Information.description.label("description"),
                Information.per.label("per"),
                Information.psr.label("psr"),
                Information.pbr.label("pbr"),
                Company.company_stock.label("company_stock"),
                Company.company_dividend.label("company_dividend"),
                Company.company_dividend_rank.label("company_dividend_rank"),
                Company.company_dividend_update.label("company_update_date"),
                Financial.sales.label("sales"),
                Financial.operating_margin.label("operating_margin"),
                Financial.eps.label("eps"),
                Financial.equity_ratio.label("equity_ratio"),
                Financial.operating_cash_flow.label("operating_cash_flow"),
                Financial.cash_and_equivalents.label("cash_and_equivalents"),
                Financial.dividend_per_share.label("dividend_per_share"),
                Financial.payout_ratio.label("payout_ratio"),
                Financial.fiscal_year.label("fiscal_year"),
            )
            .select_from(Financial)
            .outerjoin(
                Information,
                and_(
                    Financial.company_code == Information.company_code,
                ),
            )
            .outerjoin(Company, Financial.company_code == Company.company_code)
            .filter(Financial.company_code == _target_code)
        )
        rows = query.all()
        _session.close()
        return rows


class CompanyInformation(BaseDatabase):
    __tablename__ = "company_information"

    def get_information_by_code(self, code=None):
        result = []
        if code:
            rows = self._get_information_outer_join(code)
        else:
            rows = self._get_all_information_outer_join()
        for row in rows:
            if row:
                result.append({
                    "company_code": row.company_code,
                    "company_name": row.company_name,
                    'industry': row.industry,
                    'description': row.description,
                    'per': row.per,
                    'psr': row.psr,
                    'pbr': row.pbr,
                    'company_stock': row.company_stock,
                    'company_dividend': row.company_dividend,
                    'dividend_rank': row.company_dividend_rank,
                    'update_date': row.company_update_date,
                })
        return result

    @staticmethod
    def _get_information_outer_join(_target_code):
        _session = database.connect_db()
        query = (
            _session.query(
                Company.company_code.label("company_code"),
                Company.company_name.label("company_name"),
                Information.industry.label("industry"),
                Information.description.label("description"),
                Information.per.label("per"),
                Information.psr.label("psr"),
                Information.pbr.label("pbr"),
                Company.company_stock.label("company_stock"),
                Company.company_dividend.label("company_dividend"),
                Company.company_dividend_rank.label("company_dividend_rank"),
                Company.company_dividend_update.label("company_update_date"),
            )
            .select_from(Information)
            .outerjoin(Company, Information.company_code == Company.company_code)
            .filter(Information.company_code == _target_code)
        )
        rows = query.all()
        _session.close()
        return rows

    @staticmethod
    def _get_all_information_outer_join():
        _session = database.connect_db()
        query = (
            _session.query(
                Company.company_code.label("company_code"),
                Company.company_name.label("company_name"),
                Information.industry.label("industry"),
                Information.description.label("description"),
                Information.per.label("per"),
                Information.psr.label("psr"),
                Information.pbr.label("pbr"),
                Company.company_stock.label("company_stock"),
                Company.company_dividend.label("company_dividend"),
                Company.company_dividend_rank.label("company_dividend_rank"),
                Company.company_dividend_update.label("company_update_date"),
            )
            .select_from(Information)
            .outerjoin(Company, Information.company_code == Company.company_code)
        )
        rows = query.all()
        _session.close()
        return rows

    def get_information_by_code_or_name(self, code=None):
        result = []
        rows = self._get_information_outer_join_or(code)
        for row in rows:
            if row:
                result.append({
                    "company_code": row.company_code,
                    "company_name": row.company_name,
                    'industry': row.industry,
                    'description': row.description,
                    'per': row.per,
                    'psr': row.psr,
                    'pbr': row.pbr,
                    'company_stock': row.company_stock,
                    'company_dividend': row.company_dividend,
                    'dividend_rank': row.company_dividend_rank,
                    'update_date': row.company_update_date,
                })
        return result

    @staticmethod
    def _get_information_outer_join_or(search_word=None):
        _session = database.connect_db()
        select_columns = [
            Company.company_code.label("company_code"),
            Company.company_name.label("company_name"),
            Information.industry.label("industry"),
            Information.description.label("description"),
            Information.per.label("per"),
            Information.psr.label("psr"),
            Information.pbr.label("pbr"),
            Company.company_stock.label("company_stock"),
            Company.company_dividend.label("company_dividend"),
            Company.company_dividend_rank.label("company_dividend_rank"),
            Company.company_dividend_update.label("company_update_date"),
        ]
        query = (
            _session.query(*select_columns)
            .select_from(Information)
            .outerjoin(Company, Information.company_code == Company.company_code)
        )
        if search_word:
            like_word = f"%{search_word}%"
            query = query.filter(
                or_(
                    Company.company_code.like(like_word),
                    Company.company_name.like(like_word)
                )
            )
        rows = query.all()
        _session.close()
        return rows


def query_test():
    target_company_code = '9782'

    company_financial = CompanyFinancial()
    results = company_financial.get_financial_by_code(target_company_code)

    for row in results:
        print(row)


def query_information():
    target_company_code = '9782'

    company_information = CompanyInformation()
    results = company_information.get_information_by_code(target_company_code)

    for row in results:
        print(row)


if __name__ == "__main__":
    # query_test()
    query_information()
