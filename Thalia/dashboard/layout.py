import dash_core_components as dcc
import dash_html_components as html
import dash_table


def create_graph(figure, id):
    return dcc.Graph(figure=figure, id=id)


def create_table(data, columns, id):
    return dash_table.DataTable(id=id, columns=columns, data=data)


temp_tickers = [
    {"label": "Coke", "value": "COKE"},
    {"label": "Tesla", "value": "TSLA"},
    {"label": "Apple", "value": "AAPL"},
]


def create_ticker_selector(id):
    return html.Div(
        [
            dcc.Dropdown(id=id, options=temp_tickers, className="two-thirds column"),
            dcc.Input(
                id=f"{id}-proportion",
                type="number",
                min=0,
                max=100,
                className="one-third column",
            ),
        ],
        className="container",
    )


layout = html.Div(
    [
        html.H1("Stock Tickers"),
        html.Div(
            [
                html.Div([create_ticker_selector(f"ticker{i}") for i in range(1, 4)]),
                html.Button("Submit", "submit-btn"),
            ],
        ),
        html.Div(id="graph-container"),
        html.Div(id="table-container"),
    ],
    style={"width": "500"},
)
