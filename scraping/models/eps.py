from sqlalchemy import Column, Integer, Float,Date, String, UniqueConstraint
from sqlalchemy import and_, or_
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from scraping.models.db import BaseDatabase, database


class EPS(BaseDatabase):
    __tablename__ = "eps"
    company_code = Column(Integer)
    year = Column(String)
    eps = Column(Float)

    @staticmethod
    def get_or_create(code, c_year, c_eps):
        session = database.connect_db()
        row = session.query(EPS).filter(and_(
            EPS.company_code == code,
            EPS.year == c_year)).first()

        if row:
            session.close()
        else:
            sales = EPS(company_code=code,
                        year=c_year,
                        eps=c_eps)
            session.add(sales)
            session.commit()

            row = session.query(EPS).filter(and_(
                EPS.company_code == code,
                EPS.year == c_year)).first()
            session.close()
        return row


def test_EPS_DB():
    c_code = '9986'
    c_year = '2008/03'
    c_eps = '10'
    db_eps = EPS.get_or_create(
        int(c_code), c_year, c_eps)
    print(db_eps)


if __name__ == '__main__':
    test_EPS_DB()
