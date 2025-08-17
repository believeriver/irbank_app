import sys
import os
from typing import List

from sqlalchemy import Column, Integer, Float, String, BigInteger
from sqlalchemy import and_, or_

sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from scraping.models.db import BaseDatabase, database


class Financial(BaseDatabase):
    """
    1. sales: 売上高
    2. operating_margin: 営業利益率
    3. eps: EPS
    4. equity_ratio: 自己資本比率
    5. operating_cash_flow: 営業活動によるCF
    6. cash_and_equivalents: 現金など
    7. dividend_per_share: 一株配当
    8. payout_ratio: 配当性向
    9. fiscal_year: 会計年度
    """
    __tablename__ = "financials"
    company_code = Column(String(16), nullable=False)
    sales = Column(String(32), nullable=True)
    operating_margin = Column(Float, nullable=True)
    eps = Column(Float, nullable=True)
    equity_ratio = Column(Float, nullable=True)
    operating_cash_flow = Column(BigInteger, nullable=True)
    cash_and_equivalents = Column(BigInteger, nullable=True)
    dividend_per_share = Column(BigInteger, nullable=True)
    payout_ratio = Column(Float, nullable=True)
    fiscal_year = Column(String(16), nullable=True)

    @staticmethod
    def get_or_create(
            code: str,
            fiscal_year: str,
            sale: str,
            margin: float,
            eps: float,
            equity: float,
            cashflow: int,
            equivalents: int,
            dividend: int,
            payout: float):
        session = database.connect_db()
        row = session.query(Financial).filter(and_(
            Financial.company_code == code,
            Financial.fiscal_year == fiscal_year)).first()

        if row:
            row.company_code = code
            row.fiscal_year = fiscal_year
            row.sales = sale
            row.operating_margin = margin
            row.eps = eps
            row.equity_ratio = equity
            row.operating_cash_flow = cashflow
            row.cash_and_equivalents = equivalents
            row.dividend_per_share = dividend
            row.payout_ratio = payout
        else:
            financial_data = Financial(
                company_code=code,
                fiscal_year=fiscal_year,
                sales=sale,
                operating_margin=margin,
                eps=eps,
                equity_ratio=equity,
                operating_cash_flow=cashflow,
                cash_and_equivalents=equivalents,
                dividend_per_share=dividend,
                payout_ratio=payout)
            session.add(financial_data)
        session.commit()

        row = session.query(Financial).filter(and_(
            Financial.company_code == code,
            Financial.fiscal_year == fiscal_year)).first()
        session.close()
        return row

    @staticmethod
    def get_financial_by_company_code(code: str) -> List[dict]:
        result = []
        session = database.connect_db()
        row = session.query(Financial).filter(
            Financial.company_code == code).first()
        if row:
            result.append({
                "company_code": row.company_code,
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
        session.close()
        return result

    @staticmethod
    def get_financials_by_company_code(code: str) -> List[dict]:
        result = []
        session = database.connect_db()
        rows = session.query(Financial).filter(
            Financial.company_code == code).all()
        for row in rows:
            if row:
                result.append({
                    "company_code": row.company_code,
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
        session.close()
        return result


def check_financial_dbio():
    code = "2914"
    fiscal_year = "2008/03"
    sale = "6410000000000"
    margin = 6.72
    eps = 69.72
    equity = 11.33
    cashflow = 145000000000
    equivalents = 21508000000
    dividend = 0
    payout = 0
    db_financial = Financial.get_or_create(
        code, fiscal_year, sale, margin, eps, equity,
        cashflow, equivalents, dividend, payout)

    print(db_financial.company_code, db_financial.fiscal_year)
    dbo = Financial.get_financials_by_company_code(code)
    print(dbo)


if __name__ == '__main__':
    check_financial_dbio()
