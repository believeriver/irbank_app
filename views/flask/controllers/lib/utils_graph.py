import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.io as pio


def _fetch_data_frame(datasets):
    d_year = []
    data_list = [[] for _ in range(8)]
    # print(data_list)
    datasets_copy = []
    for row in datasets:
        datasets_copy.append(row)
        for idx, col in enumerate(row):
            if idx == 1:
                d_year.append(col)
            elif idx > 1:
                # if idx - 2 <= len(data_list):
                if col is not None:
                    data_list[idx - 2].append(float(col))
                else:
                    data_list[idx - 2].append(0)
    return d_year, data_list, datasets_copy


def _create_graph(df, title: str = 'title'):
    fig = px.bar(df,
                 x="year",
                 y="value",
                 title=title)
    # graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # return graph_json
    graph_html = pio.to_html(fig, full_html=False)
    return graph_html


def create_stock_graph(df, title: str = 'title'):
    fig = px.line(x=df['year'],
                  y=df['value'],
                  labels={'x': 'date', 'y': 'stock price'})
    # graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # return graph_json
    graph_html = pio.to_html(fig, full_html=False)
    return graph_html


def create_ir_graph_list(datasets):
    d_year, d_list, d_data = _fetch_data_frame(datasets)

    title_list = ["売上高",
                  "営業利益率",
                  "EPS",
                  "自己資本比率",
                  "営業活動によるCF",
                  "現金等",
                  "一株配当",
                  "配当性向"]

    fig_list = []
    for idx, data in enumerate(d_list):
        # print(data)
        d = {'year': d_year,
             'value': data}
        df = pd.DataFrame(d)
        if idx < len(title_list):
            graph_json = _create_graph(df, title_list[idx])
        else:
            graph_json = _create_graph(df)
        fig_list.append(graph_json)

    return fig_list, d_data


# graph logic test  --------------------------------------------------#
def create_graph_test1():
    df = px.data.medals_wide()
    fig = px.bar(df,
                 x="nation",
                 y=['gold', 'silver', 'bronze'],
                 title="Wide=FormInput")

    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json


def create_graph_test2():
    # graph2
    df = px.data.iris()
    fig = px.scatter_3d(df, x="sepal_length", y="sepal_width",
                         z='petal_width', color='species', title='Iris Dataset')
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json
