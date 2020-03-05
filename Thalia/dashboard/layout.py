import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html as inner_html
import os

import dash_table
from datetime import datetime as dt
import pandas as pd


df = pd.DataFrame(
    [
        {"AssetTicker": "RCK", "Name": "Rock", "Allocation": "0"},
        {"AssetTicker": "BRY", "Name": "Berry", "Allocation": "0"},
    ]
)
AssetTicker = set(df.get("AssetTicker"))


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


def ticker_selector():

    return html.Div(
        [
            html.Div(
                html.Div(
                    [
                        html.Label("Ticker: ", className="label"),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="memory_ticker",
                                    options=[
                                        {"value": x, "label": x} for x in AssetTicker
                                    ],
                                    multi=False,
                                    className="",
                                ),
                            ],
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
                        dash_table.DataTable(
                            id="memory-table",
                            columns=[
                                {
                                    "name": "AssetTicker",
                                    "id": "AssetTicker",
                                    "type": "text",
                                },
                                {"name": "Name", "id": "Name", "type": "text"},
                                {
                                    "name": "Allocation",
                                    "id": "Allocation",
                                    "type": "numeric",
                                    "editable": True,
                                },
                            ],
                            row_deletable=True,
                        )
                    ],
                    className="section",
                )
            ),
        ],
        className="columns is-marginless ",
    )


def select_dates():
    # TODO: end date should be today!
    return html.Div(
        [
            dcc.DatePickerRange(id="my-date-picker-range", max_date_allowed=dt.now(),),
            html.Div(id="date-picker-range-container"),
        ]
    )


def initial_amount_of_money():
    return html.Div(
        [
            html.I("Initial Amount"),
            html.Br(),
            dcc.Input(
                id="input_money",
                min=1,
                placeholder="Insert Initial amount of $",
                type="number",
                className="input",
            ),
            html.Div(id="output_money"),
        ]
    )


def contribution_amount():
    return html.Div(
        [
            html.I("Contribution Amount"),
            html.Br(),
            dcc.Input(
                id="input_contribution",
                placeholder="Insert contribution amount of $",
                type="number",
                className="input",
            ),
            html.Div(id="output_contribution"),
        ]
    )


def contribution_dates():
    return html.Div(
        [
            html.I("Contribution frequency"),
            html.Br(),
            dcc.Dropdown(
                id="contribution_dropdown",
                options=[  # Business month END
                    {"label": "None", "value": None},
                    {"label": "Monthly", "value": "BM"},
                    {"label": "Quarterly", "value": "BQ"},
                    {"label": "Annualy", "value": "BA"},
                    {"label": "Semi-Annualy", "value": "6BM"},
                ],
            ),
            html.Div(id="output_contribution_dpp"),
        ]
    )


def rebalancing_dates():
    return html.Div(
        [
            html.I("Rebalancing frequency"),
            html.Br(),
            dcc.Dropdown(
                id="rebalancing_dropdown",
                options=[  # Business month END
                    {"label": "None", "value": None},
                    {"label": "Monthly", "value": "BM"},
                    {"label": "Quarterly", "value": "BQ"},
                    {"label": "Annualy", "value": "BA"},
                    {"label": "Semi-Annualy", "value": "6BM"},
                ],
            ),
            html.Div(id="output_rebalancing"),
        ]
    )


def options():
    return html.Div(
        [
            html.Div(
                [
                    html.Div([select_dates()], className="container",),
                    html.Div([initial_amount_of_money()], className="container",),
                    html.Div([contribution_amount()], className="container",),
                    html.Div([contribution_dates()], className="container",),
                    html.Div([rebalancing_dates()], className="container",),
                    html.Div([ticker_selector()], className="container",),
                ]
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


def options_wrapper():
    return html.Div(
        html.Div(html.Div(options(), className="box"), className="column is-12"),
        className="columns is-multiline is-vcentered",
    )


def options_title():
    return html.Div(
        html.H1("Ticker Selection", className="title"),
        className="column is-12",
        id="tickers",
    )


def graph_box(graph_name, figure, id, size=6):
    return html.Div(
        html.Div(
            [
                html.P(graph_name, className="panel-heading"),
                html.Div(dcc.Graph(figure=figure, id=id), className="panel-block"),
            ],
            className="panel",
        ),
        className="column is-" + str(size),
    )


def box(metric_names, metric_values):
    return html.Div(
        [
            html.Div(
                [
                    html.Div(metric_names[0], className="heading"),
                    html.Div(str(metric_values[0]), className="title"),
                    html.Div(
                        [
                            box_item(metric_names[1], metric_values[1]),
                            box_item(metric_names[2], metric_values[2]),
                            box_item(metric_names[3], metric_values[3]),
                        ],
                        className="level",
                    ),
                ],
                className="box",
            )
        ],
        className="column is-4",
    )


def box_item(metric_name, metric_value):
    return html.Div(
        [
            html.Div(metric_name, className="heading"),
            html.Div(str(metric_value), className="title is-5",),
        ],
        className="level-item",
    )


def read_html(html_file):
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


def navbar():
    return html.Div(
        [
            inner_html.DangerouslySetInnerHTML(read_html("dash_navbar.html")),
            html.Hr(style={"margin-top": 0}),
        ],
    )


def level_item():
    return html.Div(
        [
            html.Div(
                html.Div(
                    html.Div("Dashboard", className="title"), className="level-item",
                ),
                className="level-left",
                id="dashboard",
            ),
            html.Div(
                html.Div(
                    html.Div(id="output_dates", className="subtitle",),
                    className="level-item",
                ),
                className="level-right",
            ),
        ],
        className="level",
    )


def main_dashboard():
    return html.Div(
        [
            box(
                ["Top Seller Total", "Sales", "Overall", "Sales %"],
                [56950, 250000, 750000, 25],
            ),
            box(
                ["Top Seller Total", "Sales", "Overall", "Sales %"],
                [56950, 250000, 750000, 25],
            ),
            box(
                ["Top Seller Total", "Sales", "Overall", "Sales %"],
                [56950, 250000, 750000, 25],
            ),
            graph_box("Overall Graph", figure={}, id="graph", size=12),
            graph_box("Another Graph", figure={}, id="graph2", size=6),
            graph_box("More Graphs", figure={}, id="graph3", size=6),
        ],
        className="columns is-multiline",
    )


layout = html.Div(
    [
        navbar(),
        html.Div(
            html.Main(
                [
                    html.Div(
                        [
                            options_title(),
                            options_wrapper(),
                            level_item(),
                            main_dashboard(),
                        ],
                        className="column is-offset-1 is-10",
                    ),
                ],
                className="columns",
            ),
            className="section",
        ),
    ]
)
