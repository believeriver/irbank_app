from sqlalchemy import Column, Integer, Float,Date, String, UniqueConstraint
from sqlalchemy import and_, or_
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from scraping.models.db import BaseDatabase, database


class CapitalAdequacy(BaseDatabase):
    __tablename__ = "capital_adequacy"
    company_code = Column(Integer)
    year = Column(String)
    ratio = Column(Float)

    @staticmethod
    def get_or_create(code, c_year, c_ratio):
        session = database.connect_db()
        row = session.query(CapitalAdequacy).filter(and_(
            CapitalAdequacy.company_code == code,
            CapitalAdequacy.year == c_year)).first()

        if row:
            session.close()
        else:
            sales = CapitalAdequacy(
                    company_code=code,
                    year=c_year,
                    ratio=c_ratio)
            session.add(sales)
            session.commit()

            row = session.query(CapitalAdequacy).filter(and_(
                CapitalAdequacy.company_code == code,
                CapitalAdequacy.year == c_year)).first()
            session.close()
        return row


def test_EPS_DB():
    c_code = '9986'
    c_year = '2008/03'
    c_ca = '41.99'
    db_eps = CapitalAdequacy.get_or_create(
        int(c_code), c_year, c_ca)
    print(db_eps)


if __name__ == '__main__':
    test_EPS_DB()
