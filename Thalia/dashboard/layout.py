import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html as inner_html
import os
import dash_table


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


def graph_box(graph_name, figure, id):
    return html.Div(
        html.Div(
            [
                html.P(graph_name, className="panel-heading"),
                html.Div(dcc.Graph(figure=figure, id=id), className="panel-block"),
            ],
            className="panel",
        ),
        className="column is-6",
    )


def box(values_dict):
    return html.Div(
        [
            html.Div(
                [
                    html.Div(list(values_dict.keys())[0], className="heading"),
                    html.Div(str(list(values_dict.values())[0]), className="title"),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        list(values_dict.keys())[1], className="heading"
                                    ),
                                    html.Div(
                                        str(list(values_dict.values())[1]),
                                        className="title is-5",
                                    ),
                                ],
                                className="level-item",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        list(values_dict.keys())[2], className="heading"
                                    ),
                                    html.Div(
                                        str(list(values_dict.values())[2]),
                                        className="title is-5",
                                    ),
                                ],
                                className="level-item",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        list(values_dict.keys())[3], className="heading"
                                    ),
                                    html.Div(
                                        str(list(values_dict.values())[3]),
                                        className="title is-5",
                                    ),
                                ],
                                className="level-item",
                            ),
                        ],
                        className="level",
                    ),
                ],
                className="box",
            )
        ],
        className="column is-4",
    )


def read_nav_html(html_file):
    base_html_path = os.path.join(
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "./templates/dash",
        ),
        html_file,
    )

    with open(base_html_path, "r") as fin:
        base_html = fin.read()

    return base_html


layout = html.Div(
    [
        html.Div(
            [
                inner_html.DangerouslySetInnerHTML(read_nav_html("dash_navbar.html")),
                html.Hr(style={"margin-top": 0}),
            ],
        ),
        html.Div(
            html.Main(
                [
                    html.Aside(
                        inner_html.DangerouslySetInnerHTML(
                            read_nav_html("dash_aside.html")
                        ),
                        className="column is-2",
                    ),
                    html.Div(
                        [
                            html.Div(
                                html.H1("Ticker Selection", className="title"),
                                className="column is-12",
                                id="tickers",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        html.Div(options(), className="box"),
                                        className="column is-12",
                                    ),
                                ],
                                className="columns is-multiline is-vcentered",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        html.Div(
                                            html.Div("Dashboard", className="title"),
                                            className="level-item",
                                        ),
                                        className="level-left",
                                        id="dashboard",
                                    ),
                                    html.Div(
                                        html.Div(
                                            html.Div(
                                                "March 8, 2017 - April 6, 2017",
                                                className="subtitle",
                                            ),
                                            className="level-item",
                                        ),
                                        className="level-right",
                                    ),
                                ],
                                className="level",
                            ),
                            html.Div(
                                [
                                    box(
                                        {
                                            "Top Seller Total": 56950,
                                            "Sales": 250000,
                                            "Overall": 750000,
                                            "Sales %": 25,
                                        }
                                    ),
                                    box(
                                        {
                                            "Top Seller Total": 56950,
                                            "Sales": 250000,
                                            "Overall": 750000,
                                            "Sales %": 25,
                                        }
                                    ),
                                    box(
                                        {
                                            "Top Seller Total": 56950,
                                            "Sales": 250000,
                                            "Overall": 750000,
                                            "Sales %": 25,
                                        }
                                    ),
                                    graph_box("Overall Graph", figure={}, id="graph"),
                                    graph_box("Another Graph", figure={}, id="graph2"),
                                    graph_box("More Graphs", figure={}, id="graph3"),
                                    graph_box(
                                        "Graphs Graphs Graphs", figure={}, id="graph4"
                                    ),
                                ],
                                className="columns is-multiline",
                            ),
                        ],
                        className="column is-10",
                    ),
                ],
                className="columns",
            ),
            className="section",
        ),
    ]
)
