import dash_core_components as dcc
import dash_html_components as html
import dash_table


def graph(figure, id):
    """
    exists purely to be called from callbacks

    TODO: evaluate if antipattern? wrong type of abstraction?
    """
    return dcc.Graph(figure=figure, id=id)


def table(data, id):
    """
    exists purely to be called from callbacks

    TODO: evaluate if antipattern? wrong type of abstraction?
    """
    columns = [
        {"name": "metric", "id": "metric"},
        {"name": "value", "id": "value"},
    ]
    return dash_table.DataTable(id=id, columns=columns, data=data)


def ticker_selector(id):
    tickers = [
        {"label": "Coke", "value": "COKE"},
        {"label": "Tesla", "value": "TSLA"},
        {"label": "Apple", "value": "AAPL"},
    ]
    return html.Div(
        [
            html.Div(
                html.Div(
                    [
                        html.Label("Ticker: ", className="label"),
                        html.Div(
                            dcc.Dropdown(id=id, options=tickers, className=""),
                            className="control",
                        ),
                    ],
                    className="field",
                ),
                className="column",
            ),
            html.Div(
                html.Div(
                    [
                        html.Label("Allocation: ", className="label"),
                        html.Div(
                            dcc.Input(
                                id=f"{id}-proportion",
                                type="number",
                                min=0,
                                max=100,
                                className="input",
                            ),
                            className="control",
                        ),
                    ],
                    className="field",
                ),
                className="column",
            ),
        ],
        className="columns is-marginless ",
    )


def options():
    return html.Div(
        [
            html.Div(
                [ticker_selector(f"ticker{i}") for i in range(1, 4)],
                className="container",
            ),
            html.Button("Submit", "submit-btn", className="button is-large is-primary"),
        ],
        className="container",
    )


layout = html.Div(
    # essentially the applications main HTML layout
    html.Div(
        [
            html.H1("Stock Tickers", className="title"),
            options(),
            dcc.Loading(
                [graph({}, id="graph"), table([], "table")], className="container"
            ),
        ],
        className="section",
    )
)
