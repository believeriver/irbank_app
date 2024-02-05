from sqlalchemy import Column, Integer, Float,Date, String, UniqueConstraint
from sqlalchemy import and_, or_
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from scraping.models.db import BaseDatabase, database


class Margins(BaseDatabase):
    __tablename__ = "operating_margins"
    company_code = Column(Integer)
    year = Column(String)
    margin = Column(Float)

    @staticmethod
    def get_or_create(code, c_year, c_margin):
        session = database.connect_db()
        row = session.query(Margins).filter(and_(
            Margins.company_code == code,
            Margins.year == c_year)).first()

        if row:
            session.close()
        else:
            sales = Margins(company_code=code,
                            year=c_year,
                            margin=c_margin)
            session.add(sales)
            session.commit()

            row = session.query(Margins).filter(and_(
                Margins.company_code == code,
                Margins.year == c_year)).first()
            session.close()
        return row


def test_Margins_DB():
    c_code = '9986'
    c_year = '2008/03'
    c_sales = '14.5'
    op_margin = Margins.get_or_create(
        int(c_code), c_year, c_sales)
    print(op_margin)


if __name__ == '__main__':
    test_Margins_DB()
