from sqlalchemy import Column, Integer, Float,Date, String, UniqueConstraint
from sqlalchemy import and_, or_
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from scraping.models.db import BaseDatabase, database


class Sales(BaseDatabase):
    __tablename__ = "sales"
    company_code = Column(Integer)
    year = Column(String)
    amount_sales = Column(String)

    @staticmethod
    def get_or_create(code, c_year, c_sales):
        session = database.connect_db()
        row = session.query(Sales).filter(and_(
            Sales.company_code == code,
            Sales.year == c_year)).first()

        if row:
            session.close()
        else:
            sales = Sales(company_code=code,
                          year=c_year,
                          amount_sales=c_sales)
            session.add(sales)
            session.commit()

            row = session.query(Sales).filter(and_(
                Sales.company_code == code,
                Sales.year == c_year)).first()
            session.close()
        return row


def test_Sales_DB():
    c_code = '9986'
    c_year = '2008/03'
    c_sales = '6529590000'
    sales = Sales.get_or_create(
        int(c_code), c_year, c_sales)
    # print(sales)


if __name__ == '__main__':
    test_Sales_DB()
