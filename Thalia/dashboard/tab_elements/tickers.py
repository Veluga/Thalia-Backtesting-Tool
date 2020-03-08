import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd
from datetime import datetime as dt

MIN_TICKERS = 3
df = pd.DataFrame(
    [
        {"AssetTicker": "RCK", "Name": "Rock", "Allocation": "0"},
        {"AssetTicker": "BRY", "Name": "Berry", "Allocation": "0"},
    ]
)
AssetTicker = set(df.get("AssetTicker"))

"""
def ticker_selector(id):
    return html.Div(
        [
            html.Div(
                html.Div(
                    [
                        html.Label("Ticker: ", className="label"),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="memory-ticker-" + str(id),
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
                            id="memory-table-" + str(id),
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
"""


def ticker_selector(portfolio_id, ticker_id):
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
                            dcc.Dropdown(
                                id=f"ticker-{portfolio_id}-{ticker_id}",
                                options=tickers,
                                className="",
                            ),
                            className="control",
                        ),
                    ],
                    className="field",
                ),
                className="column is-6",
            ),
            html.Div(
                html.Div(
                    [
                        html.Label("Allocation: ", className="label"),
                        html.Div(
                            dcc.Input(
                                id=f"proportion-{portfolio_id}-{ticker_id}",
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
                className="column is-6",
            ),
        ],
        className="columns is-marginless is-multiline",
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
                id="input-money",
                min=1,
                placeholder="Insert Initial amount of $",
                type="number",
                className="input",
            ),
            html.Div(id="output-money"),
        ]
    )


def contribution_amount(id):
    return html.Div(
        [
            html.I("Contribution Amount"),
            html.Br(),
            dcc.Input(
                id="input-contribution-" + str(id),
                placeholder="Insert contribution amount of $",
                type="number",
                className="input",
            ),
            html.Div(id="output-contribution-" + str(id)),
        ]
    )


def contribution_dates(id):
    return html.Div(
        [
            html.I("Contribution frequency"),
            html.Br(),
            dcc.Dropdown(
                id="contribution-dropdown-" + str(id),
                options=[  # Business month END
                    {"label": "None", "value": None},
                    {"label": "Monthly", "value": "BM"},
                    {"label": "Quarterly", "value": "BQ"},
                    {"label": "Annualy", "value": "BA"},
                    {"label": "Semi-Annualy", "value": "6BM"},
                ],
            ),
            html.Div(id="output-contribution-dpp-" + str(id)),
        ]
    )


def rebalancing_dates(id):
    return html.Div(
        [
            html.I("Rebalancing frequency"),
            html.Br(),
            dcc.Dropdown(
                id="rebalancing-dropdown-" + str(id),
                options=[  # Business month END
                    {"label": "None", "value": None},
                    {"label": "Monthly", "value": "BM"},
                    {"label": "Quarterly", "value": "BQ"},
                    {"label": "Annualy", "value": "BA"},
                    {"label": "Semi-Annualy", "value": "6BM"},
                ],
            ),
            html.Div(id="output-rebalancing-" + str(id)),
        ]
    )


def lazy_portfolios(id):
    return dcc.Dropdown(
        id="lazy-portfolios-" + str(id),
        placeholder="Lazy",
        className="has-text-left",
        options=[  # Business month END
            {"label": "None", "value": None},
            {"label": "Lazy 1", "value": "Lazy 1"},
            {"label": "Lazy 2", "value": "Lazy 2"},
            {"label": "Lazy 3", "value": "Lazy 3"},
            {"label": "Lazy 4", "value": "Lazy 4"},
        ],
    )


def options(id):
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        dcc.Input(
                            placeholder="Portfolio " + str(id),
                            type="text",
                            value="Portfolio " + str(id),
                            style={
                                "border-width": "0px",
                                "color": "#363636",
                                "font-size": "2rem",
                                "font-weight": "600",
                                "line-height": "1.125",
                                "padding-bottom": "0.5cm",
                            },
                        ),
                        className="column is-11 has-text-left",
                    ),
                    html.Div(
                        lazy_portfolios(id), className="column is-1 has-text-right"
                    ),
                    html.Div([contribution_amount(id)], className="column is-12"),
                    html.Div([contribution_dates(id)], className="column is-12"),
                    html.Div([rebalancing_dates(id)], className="column is-12"),
                    html.Div(
                        [ticker_selector(id, i) for i in range(MIN_TICKERS)],
                        className="column is-12",
                        id=f"tickers-container-{id}",
                    ),
                    add_asset_button(id),
                ],
                className="columns is-multiline",
            )
        ],
        className="box",
    )


def submit_button():
    return html.Div(
        html.Button(
            "Submit",
            "submit-btn",
            className="button is-large is-primary",
            style={"background-color": "#f26a4b"},
        ),
        className="container has-text-centered",
    )


def add_portfolio_button():
    return html.Div(
        html.Button(
            "Add Portfolio",
            "add-portfolio-btn",
            className="button is-medium",
            style={
                "border": "0px",
                "color": "#f26a4b",
                "background-color": "transparent",
            },
        )
    )


def add_asset_button(id):
    return html.Div(
        html.Button(
            "Add Asset",
            id=f"add-asset-btn-{id}",
            className="button is-small",
            style={
                "border": "0px",
                "color": "#f26a4b",
                "background-color": "transparent",
            },
        )
    )


def options_wrapper():
    return html.Div(
        [
            html.Div(
                [html.Div([select_dates()]), html.Div([initial_amount_of_money()],),],
                className="box",
            ),
            html.Div(children=[options(1),], id="portfolios-container"),
            add_portfolio_button(),
            html.Br(),
            submit_button(),
        ],
        id="portfolios-main",
    )
