from sqlalchemy import Column, Integer, Float,Date, String, UniqueConstraint
from sqlalchemy import and_, or_
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from scraping.models.db import BaseDatabase, database


class CashDividend(BaseDatabase):
    __tablename__ = "cash_dividends"
    company_code = Column(Integer)
    year = Column(String)
    cash = Column(Integer)

    @staticmethod
    def get_or_create(code, c_year, c_cash):
        session = database.connect_db()
        row = session.query(CashDividend).filter(and_(
            CashDividend.company_code == code,
            CashDividend.year == c_year)).first()

        if row:
            session.close()
        else:
            sales = CashDividend(
                    company_code=code,
                    year=c_year,
                    cash=c_cash)
            session.add(sales)
            session.commit()

            row = session.query(CashDividend).filter(and_(
                CashDividend.company_code == code,
                CashDividend.year == c_year)).first()
            session.close()
        return row


def test_DB():
    c_code = '9986'
    c_year = '2008/03'
    c_ca = '365'
    db = CashDividend.get_or_create(
        int(c_code), c_year, c_ca)
    print('db', db)


if __name__ == '__main__':
    test_DB()
