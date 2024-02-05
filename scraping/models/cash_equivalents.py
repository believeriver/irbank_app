from sqlalchemy import Column, Integer, Float,Date, String, UniqueConstraint
from sqlalchemy import and_, or_
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from scraping.models.db import BaseDatabase, database


class CashEquivalents(BaseDatabase):
    __tablename__ = "cash_equivalents"
    company_code = Column(Integer)
    year = Column(String)
    cash = Column(Integer)

    @staticmethod
    def get_or_create(code, c_year, c_cash):
        session = database.connect_db()
        row = session.query(CashEquivalents).filter(and_(
            CashEquivalents.company_code == code,
            CashEquivalents.year == c_year)).first()

        if row:
            session.close()
        else:
            sales = CashEquivalents(
                    company_code=code,
                    year=c_year,
                    cash=c_cash)
            session.add(sales)
            session.commit()

            row = session.query(CashEquivalents).filter(and_(
                CashEquivalents.company_code == code,
                CashEquivalents.year == c_year)).first()
            session.close()
        return row


def test_DB():
    c_code = '9986'
    c_year = '2008/03'
    c_ca = '16886000000'
    db = CashEquivalents.get_or_create(
        int(c_code), c_year, c_ca)
    print(db)


if __name__ == '__main__':
    test_DB()
