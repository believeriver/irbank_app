from sqlalchemy import Column, Integer, Float, DateTime, String, UniqueConstraint
# from sqlalchemy import and_, or_
import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from scraping.models.db import BaseDatabase, database


class Information(BaseDatabase):
    __tablename__ = "informations"
    company_code = Column(String(16), nullable=False)
    industry = Column(String(10), nullable=True)
    description = Column(String(255), nullable=True)
    per = Column(Float, nullable=True)
    psr = Column(Float, nullable=True)
    pbr = Column(Float, nullable=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    @staticmethod
    def get_or_create(code, c_industry, c_description, c_per, c_psr, c_pbr):
        session = database.connect_db()
        row = session.query(Information).filter(
            Information.company_code == code).first()

        if row is None:
            # 新規作成
            row = Information(
                company_code=code,
                industry=c_industry,
                description=c_description,
                per=c_per,
                psr=c_psr,
                pbr=c_pbr
            )
            session.add(row)
        else:
            # 既存レコードを更新
            row.industry = c_industry
            row.description = c_description
            row.per = c_per
            row.psr = c_psr
            row.pbr = c_pbr

        session.commit()

        row = session.query(Information).filter(
            Information.company_code == code).first()
        session.close()
        return row


def check_information_db():
    c_code = '9219'
    c_industry = 'サービス業'
    c_description = '企業コンサル事業。データ分析を駆使した営業や業務効率化支援など。ツール提供。'
    c_per = 58.86
    c_psr = 2.45
    c_pbr = 2.65
    db_info = Information.get_or_create(
        c_code, c_industry, c_description, c_per, c_psr, c_pbr)
    print(db_info.company_code, db_info.description, db_info.updated_at)


if __name__ == '__main__':
    check_information_db()
