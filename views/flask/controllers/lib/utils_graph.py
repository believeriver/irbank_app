import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.io as pio


def create_stock_graph(df, title: str = 'title'):
    fig = px.line(x=df['year'],
                  y=df['value'],
                  title=title,
                  labels={'x': 'date', 'y': 'stock price'})
    graph_html = pio.to_html(fig, full_html=False)
    return graph_html


def _create_graph(df, title: str = 'title'):
    fig = px.bar(df,
                 x="year",
                 y="value",
                 title=title)
    graph_html = pio.to_html(fig, full_html=False)
    return graph_html


def _fetch_data_from_pandas(datasets: pd.DataFrame):
    # print({'_fetch_data_from_pandas': datasets})
    x_axis = "年"
    itme_list = ["売上高(円)", "営業利益率(%)", "EPS", "自己資本率(%)",
                 "営業活動によるCF(円)", "現金等(円)", "一株配当(円)", "配当性向(%)"]
    d_list = []
    for item in itme_list:
        try:
            d_list.append([item, datasets[[x_axis, item]]])
        except Exception as e:
            print({'[error] _fetch_data_pandas': e})

    # print({'d_list': d_list})
    return d_list


def create_ir_graph_list_df(datasets):
    d_list = _fetch_data_from_pandas(datasets)

    fig_list = []
    for item in d_list:
        title = item[0]
        d = {'year': item[1].iloc[:, 0],
             'value': item[1].iloc[:, 1]}
        df = pd.DataFrame(d)
        graph_html = _create_graph(df, title)
        fig_list.append(graph_html)

    return fig_list, datasets

