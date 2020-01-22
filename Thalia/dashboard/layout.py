import dash_core_components as dcc
import dash_html_components as html
import dash_table


def create_graph(figure, id):
    return dcc.Graph(figure=figure, id=id)


def create_table(data, columns, id):
    return dash_table.DataTable(id=id, columns=columns, data=data)


temp_tickers = [{"label": "Coke", "value": "COKE"},
                {"label": "Tesla", "value": "TSLA"},
                {"label": "Apple", "value": "AAPL"}]

layout = html.Div(
    [
        html.H1("Stock Tickers"),
        dcc.Dropdown(id="ticker1", options=temp_tickers),
        dcc.Input(id="ticker1-proportion", type='number', min=0, max=100),
        dcc.Dropdown(id="ticker2", options=temp_tickers),
        dcc.Input(id="ticker2-proportion", type='number', min=0, max=100),
        dcc.Dropdown(id="ticker3", options=temp_tickers),
        dcc.Input(id="ticker3-proportion", type='number', min=0, max=100),
        html.Button('Submit', 'submit-btn'),
        html.Div(id="graph-container"),
        html.Div(id="table-container"),
    ],
    style={"width": "500"},
)
