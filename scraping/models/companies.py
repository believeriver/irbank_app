from typing import List
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy import and_, or_
import sys
import os

app_path = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
sys.path.append(app_path)

from scraping.models.db import BaseDatabase, database


class Company(BaseDatabase):
    __tablename__ = "companies"
    company_code = Column(String(16), nullable=False)
    company_name = Column(String(100), nullable=False)
    company_stock = Column(String(32), nullable=False)
    company_dividend = Column(Float, nullable=False)
    company_dividend_rank = Column(Integer, nullable=False)
    company_dividend_update = Column(String(100), nullable=False)

    @staticmethod
    def get_or_create(c_code, c_name, c_stock, c_dividend, c_rank, c_date):
        session = database.connect_db()
        row = session.query(Company).filter(
            Company.company_code == c_code).first()

        if row:
            row_update = session.query(Company).filter(and_(
                Company.company_code == c_code,
                Company.company_dividend_update == c_date)).first()
            if row_update:
                session.close()
            else:
                row.company_stock = c_stock
                row.company_dividend = c_dividend
                row.company_dividend_rank = c_rank
                row.company_dividend_update = c_date
                session.add(row)
                session.commit()

                row = session.query(Company).filter(
                    Company.company_code == c_code).first()
                session.close()
        else:
            company = Company(
                company_code=c_code,
                company_name=c_name,
                company_stock=c_stock,
                company_dividend=c_dividend,
                company_dividend_rank=c_rank,
                company_dividend_update=c_date)
            session.add(company)
            session.commit()

            row = session.query(Company).filter(
                Company.company_code == c_code).first()
            session.close()
        return row

    @staticmethod
    def fetch_code_and_name() -> List[dict]:
        result = []
        session = database.connect_db()
        rows = session.query(Company).all()
        for row in rows:
            # print(row.company_name)
            result.append({
                'company_code': row.company_code,
                'company_name': row.company_name,
                'company_stock': row.company_stock,
                'company_dividend': row.company_dividend,
                'dividend_rank': row.company_dividend_rank,
                'update_date': row.company_dividend_update
            })
        return result

    @staticmethod
    def fetch_code_and_name_one(c_code) -> List[dict]:
        result = []
        session = database.connect_db()
        # rows = session.query(Company).all()
        row = session.query(Company).filter(
            Company.company_code == c_code).first()
        if row:
            result.append({
                'company_code': row.company_code,
                'company_name': row.company_name,
                'company_stock': row.company_stock,
                'company_dividend': row.company_dividend,
                'dividend_rank': row.company_dividend_rank,
                'update_date': row.company_dividend_update
            })
        return result

    @staticmethod
    def fetch_code_and_name_by_name(partial_name: str) -> List[dict]:
        result = []
        session = database.connect_db()
        # 部分一致（LIKE）検索
        rows = session.query(Company).filter(
            Company.company_name.like(f'%{partial_name}%')
        ).all()
        for row in rows:
            result.append({
                'company_code': row.company_code,
                'company_name': row.company_name,
                'company_stock': row.company_stock,
                'company_dividend': row.company_dividend,
                'dividend_rank': row.company_dividend_rank,
                'update_date': row.company_dividend_update
            })
        return result


def check_company_db():
    c_code = '9986'
    c_name = '蔵王産業'
    c_stock = '2400'
    c_dividend = '4.355'
    c_rank = '50'
    c_date = '更新日時：2023/08/25 18:40'
    company = Company.get_or_create(
        c_code, c_name, c_stock, float(c_dividend), int(c_rank), c_date
    )
    data = Company.fetch_code_and_name()
    print(data)
    print(
        company.company_code, company.company_name, company.company_dividend, company.company_dividend_update)

    print(Company.fetch_code_and_name_one('9219'))


if __name__ == '__main__':
    check_company_db()
