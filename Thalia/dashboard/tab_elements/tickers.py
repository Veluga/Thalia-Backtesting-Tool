import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd
from datetime import datetime as dt


df = pd.DataFrame(
    [
        {"AssetTicker": "RCK", "Name": "Rock", "Allocation": "0"},
        {"AssetTicker": "BRY", "Name": "Berry", "Allocation": "0"},
    ]
)
AssetTicker = set(df.get("AssetTicker"))


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
        ],
        className="container has-text-centered",
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
            html.Div([select_dates()],),
            html.Div([initial_amount_of_money()],),
            html.Div([contribution_amount()],),
            html.Div([contribution_dates()],),
            html.Div([rebalancing_dates()],),
            html.Div([ticker_selector()],),
        ]
    )


def submit_button():
    return html.Div(
        html.Button(
            "Submit",
            "submit-btn",
            className="button is-medium is-primary",
            style={"background-color": "#f26a4b"},
        ),
        className="container has-text-centered",
    )


def options_wrapper():
    return html.Div([options(), html.Br(), submit_button(),], className="box",)
