import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.io as pio

pio.templates.default = "plotly_dark"


def create_stock_graph(df, title: str = 'title'):
    fig = px.line(x=df['year'],
                  y=df['value'],
                  title=title,
                  labels={'x': 'date', 'y': 'stock price'})

    graph_html = pio.to_html(fig,
                             full_html=False,
                             config={"responsive": True,
                                     "staticPlot": True},
                             default_width='100%')

    return graph_html


def _create_graph(df, title: str = 'title'):
    fig = px.bar(df,
                 x="year",
                 y="value",
                 title=title,)

    fig.update_traces(
        textposition='outside',
        marker_line_width=0
    )

    fig.update_layout(
        font_family='Montserrat, Arial, sans-serif',
        font_size=15,
        font_color='#eaeaea',
        title_font_size=20,
        plot_bgcolor='rgba(18,20,25,1)',
        paper_bgcolor='rgba(10,12,15,1)',
        xaxis=dict(showgrid=False, zeroline=False, linecolor='rgba(255,255,255,0.1)', tickfont=dict(size=16)),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', zeroline=False, tickfont=dict(size=16)),
        margin=dict(t=90, l=60, r=40, b=60)
    )

    graph_html = pio.to_html(fig,
                             full_html=False,
                             config={"responsive": True,
                                     "staticPlot": True},
                             default_width='100%')
    return graph_html


def _fetch_data_from_pandas(datasets: pd.DataFrame):
    # print({'_fetch_data_from_pandas': datasets})
    x_axis = "年"
    item_list = [
        "売上高(円)",
        "営業利益率(%)",
        "EPS",
        "自己資本率(%)",
        "営業活動によるCF(円)",
        "現金等(円)",
        "一株配当(円)",
        "配当性向(%)"]
    d_list = []
    for item in item_list:
        try:
            d_list.append([item, datasets[[x_axis, item]]])
        except Exception as e:
            print({'[error] _fetch_data_pandas': e})

    # print({'d_list': d_list})
    return d_list


def create_ir_graph_list_df(datasets):
    d_list = _fetch_data_from_pandas(datasets)

    fig_list = []
    explains = {
        "売上高(円)": "売上高(円):　ブレが小さく右肩上がりか？",
        "営業利益率(%)": "営業利益率(%): １０％以上か？",
        "EPS": "EPS:　一株当たり利益は右肩上がりか？",
        "自己資本率(%)": "自己資本率(%):　最低４０％以上,６０％以上理想的,８０％以上最高",
        "営業活動によるCF(円)": "営業活動によるCF(円):　毎期黒字で右肩上がりか？",
        "現金等(円)": "現金等(円):　増えていくのが理想的",
        "一株配当(円)": "一株配当(円):　安定性と成長性を確認する",
        "配当性向(%)": "配当性向(%):　３０〜５０％が健全。高過ぎ注意。",
    }
    for item in d_list:
        title = explains.get(item[0])
        d = {'year': item[1].iloc[:, 0],
             'value': item[1].iloc[:, 1]}
        df = pd.DataFrame(d)
        graph_html = _create_graph(df, title)
        fig_list.append(graph_html)

    return fig_list, datasets

