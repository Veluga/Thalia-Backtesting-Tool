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


def ticker_selector(count):
    return html.Div(
        [
            html.Div(
                html.Div(
                    [
                        html.Label("Ticker: ", className="label"),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="memory-ticker-" + str(count),
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
                            id="memory-table-" + str(count),
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
                id="input-money",
                min=1,
                placeholder="Insert Initial amount of $",
                type="number",
                className="input",
            ),
            html.Div(id="output-money"),
        ]
    )


def contribution_amount(count):
    return html.Div(
        [
            html.I("Contribution Amount"),
            html.Br(),
            dcc.Input(
                id="input-contribution-" + str(count),
                placeholder="Insert contribution amount of $",
                type="number",
                className="input",
            ),
            html.Div(id="output-contribution-" + str(count)),
        ]
    )


def contribution_dates(count):
    return html.Div(
        [
            html.I("Contribution frequency"),
            html.Br(),
            dcc.Dropdown(
                id="contribution-dropdown-" + str(count),
                options=[  # Business month END
                    {"label": "None", "value": None},
                    {"label": "Monthly", "value": "BM"},
                    {"label": "Quarterly", "value": "BQ"},
                    {"label": "Annualy", "value": "BA"},
                    {"label": "Semi-Annualy", "value": "6BM"},
                ],
            ),
            html.Div(id="output-contribution-dpp-" + str(count)),
        ]
    )


def rebalancing_dates(count):
    return html.Div(
        [
            html.I("Rebalancing frequency"),
            html.Br(),
            dcc.Dropdown(
                id="rebalancing-dropdown-" + str(count),
                options=[  # Business month END
                    {"label": "None", "value": None},
                    {"label": "Monthly", "value": "BM"},
                    {"label": "Quarterly", "value": "BQ"},
                    {"label": "Annualy", "value": "BA"},
                    {"label": "Semi-Annualy", "value": "6BM"},
                ],
            ),
            html.Div(id="output-rebalancing-" + str(count)),
        ]
    )


def lazy_portfolios(count):
    return dcc.Dropdown(
        id="lazy-portfolios-" + str(count),
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


def options(count):
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        dcc.Input(
                            placeholder="Portfolio " + str(count),
                            type="text",
                            value="Portfolio " + str(count),
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
                        lazy_portfolios(count), className="column is-1 has-text-right"
                    ),
                    html.Div([contribution_amount(count)], className="column is-12"),
                    html.Div([contribution_dates(count)], className="column is-12"),
                    html.Div([rebalancing_dates(count)], className="column is-12"),
                    html.Div([ticker_selector(count)], className="column is-12"),
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
            className="button is-medium is-primary",
            style={"background-color": "#f26a4b"},
        ),
        className="container has-text-centered",
    )


def add_portfolio_button():
    return html.Div(
        html.Button(
            "Add Portfolio", "add-portfolio-btn", className="button is-small is-link"
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
