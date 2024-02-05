import logging
import os
import sys

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(PROJECT_PATH)
sys.path.append(PROJECT_PATH)

import pandas as pd
import streamlit as st

from sqlite3db.controllers.dao_fetch_japanstock import IRBankDB
from sqlite3db.controllers.dao_fetch_companies import Companies, FetchCompany, SearchCompanyCode

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


@st.cache_data
def fetch_japan_ir_bank_database(code) -> [pd.DataFrame, pd.DataFrame]:
    db = IRBankDB()

    try:
        _ir_bank_df = db.fetch_company_ir_dataset(code)
    except:
        st.error('IR データの取得でエラーが発生しました')
        _ir_bank_df = None

    try:
        _stock_df = db.fetch_stock_price_data(code)
    except:
        st.error('yahoo financeのデータ取得でエラーが発生しました')
        _stock_df = None

    return _ir_bank_df, _stock_df


def fetch_company_code(_company_name) -> pd.DataFrame:
    if _company_name == '':
        return None

    db = SearchCompanyCode()
    try:
        _company_df = db.fetch_company_dataset(_company_name)
        if _company_df.empty:
            return '該当なし'
        # logging.info({'action': 'fetch_company_code', '_company_df': _company_df})
        return _company_df
    except Exception as e:
        st.sidebar.error(e, '企業コードの検索でエラーが発生しました')
        return None


def create_bar_chart(item, _ir_bank_df,):
    try:
        st.write(f'#### {item}')
        df_bar = pd.DataFrame([_ir_bank_df['年'], _ir_bank_df[item]])
        df_bar = df_bar.T
        st.bar_chart(df_bar.set_index('年'))
    except:
        st.error(f"{item}はデータがありません")


def start_streamlit_db():
    st.title('日本高配当株価可視化アプリ')

    # sidebar
    st.sidebar.write("""
            # 日本高配当株価
            こちらはIR情報と株価可視化ツールです。以下のオプションから企業コードを指定
        """)

    st.sidebar.write("""
            ## 企業コードの入力
            """)
    company = st.sidebar.text_input('日本株企業コードを入力してください')

    st.sidebar.divider()
    st.sidebar.write("""
        #### 企業コードがわからない場合は、以下で検索できます。
    """)
    search_company_name = st.sidebar.text_input('日本企業名を入力してください')
    search_company_code = fetch_company_code(search_company_name)
    st.sidebar.write(search_company_code)

    st.sidebar.text('参考')
    link_yahoo = '[Yahoo 日本高配当利回りランキング](https://finance.yahoo.co.jp/stocks/ranking/dividendYield?market=all)'
    st.sidebar.markdown(link_yahoo, unsafe_allow_html=True)
    link_ir_bank = '[IR BANK](https://irbank.net/)'
    st.sidebar.markdown(link_ir_bank, unsafe_allow_html=True)

    # main
    if company == '':
        companies_dataset = Companies()
        df = companies_dataset.companies_dataset()
        st.write(df)
    else:
        try:
            company = int(company)
        except:
            st.error('企業コードは４桁の数字で入力ください')

        try:
            # print('company: ', company)
            logging.info({'company_code': company})
            company_dataset = FetchCompany()
            df = company_dataset.fetch_company_dataset(int(company))
            if df.empty:
                st.error('データがありません。')
            else:
                ir_bank_df, stock_df = fetch_japan_ir_bank_database(company)
                stock_df = stock_df.set_index('year')
                stock_df = stock_df.rename(columns={'value': 'Stock Price(yen)'})
                st.write('### 企業名と配当率', df)
                # st.write('### IRBANK情報抽出', ir_bank_df)
                # st.write('### Y financeより株価(円)データ', stock_df)

                st.write('### yahoo financeより株価（円）のトレンドグラフ')
                st.line_chart(stock_df)

                st.write('### IR 参考情報')
                create_bar_chart('売上高(円)', ir_bank_df)
                create_bar_chart('営業利益率(%)', ir_bank_df)
                create_bar_chart('EPS', ir_bank_df)
                create_bar_chart('自己資本率(%)', ir_bank_df)
                create_bar_chart('営業活動によるCF(円)', ir_bank_df)
                create_bar_chart('現金等(円)', ir_bank_df)
                create_bar_chart('一株配当(円)', ir_bank_df)
                create_bar_chart('配当性向(%)', ir_bank_df)

        except Exception as e:
            st.error("何かエラーが発生しました。企業コードなどを確認してください。")


if __name__ == '__main__':
    start_streamlit_db()

