import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html as inner_html
import os
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
            html.Br(),
            html.Div(
                html.Button(
                    "Submit",
                    "submit-btn",
                    className="button is-medium is-primary",
                    style={"background-color": "#f26a4b"},
                ),
                className="container has-text-centered",
            ),
        ],
        className="container",
    )


def read_nav_html():
    base_html_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "./templates/dash_navbar.html",
    )

    with open(base_html_path, "r") as fin:
        base_html = fin.read()

    return base_html


layout = html.Div(
    [
        html.Div(
            [
                inner_html.DangerouslySetInnerHTML(read_nav_html()),
                html.Hr(style={"margin-top": 0}),
            ]
        ),
        html.Main(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    html.H1("Dashboard", className="title"),
                                    className="container",
                                ),
                            ],
                            className="column is-12",
                        ),
                        html.Div(options(), className="column is-12"),
                        dcc.Loading(graph({}, id="graph"), className="column is-9"),
                        dcc.Loading(table([], "table"), className="column"),
                    ],
                    className="columns is-multiline is-vcentered",
                ),
            ],
            className="column",
        ),
    ]
)
