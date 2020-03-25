import dash_html_components as html
import dash_core_components as dcc
import dash_table
from datetime import datetime as dt
from .. import util


def ticker_dropdown(id):
    tickers = util.get_asset_names()
    return html.Div(
        html.Div(
            [
                html.Label("Ticker: ", className="label"),
                html.Div(
                    [
                        dcc.Dropdown(
                            id=f"memory-ticker-{id}",
                            options=[{"value": x, "label": x} for x in tickers],
                            multi=False,
                            className="",
                        ),
                    ],
                    className="control",
                ),
            ],
            className="field",
        ),
        className="column is-6 is-offset-3",
    )


def ticker_table(id):
    return html.Div(
        html.Div(
            [
                dash_table.DataTable(
                    id=f"memory-table-{id}",
                    columns=[
                        {"name": "AssetTicker", "id": "AssetTicker", "type": "text",},
                        {"name": "Name", "id": "Name", "type": "text"},
                        {
                            "name": "Allocation",
                            "id": "Allocation",
                            "type": "numeric",
                            "editable": True,
                        },
                    ],
                    row_deletable=True,
                    style_data_conditional=[
                        {
                            "if": {"row_index": "odd"},
                            "backgroundColor": "rgb(248, 248, 248)",
                        },
                        {
                            "if": {
                                "column_id": "Allocation",
                                "filter_query": "{Allocation} > 100",
                            },
                            "backgroundColor": "#f26a4b",
                            "color": "white",
                        },
                    ],
                    style_header={
                        "backgroundColor": "rgb(230, 230, 230)",
                        "fontWeight": "bold",
                    },
                    style_cell_conditional=[{"textAlign": "center"}],
                )
            ],
            className="section",
        ),
        className="column is-4 is-offset-4",
    )


def ticker_selector(id):
    return html.Div(
        [ticker_dropdown(id), ticker_table(id),],
        className="columns is-marginless is-multiline",
    )


def select_dates():
    # TODO: end date should be today!
    today = dt.now().date()
    return html.Div(
        [
            dcc.DatePickerRange(
                id="my-date-picker-range",
                max_date_allowed=today,
                start_date="1970-01-01",
                end_date=today,
            ),
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
                value=1000,
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
                id=f"input-contribution-{id}",
                placeholder="Insert contribution amount of $",
                type="number",
                className="input",
            ),
            html.Div(id=f"output-contribution-{id}"),
        ]
    )


def contribution_dates(id):
    return html.Div(
        [
            html.I("Contribution frequency"),
            html.Br(),
            dcc.Dropdown(
                id=f"contribution-dropdown-{id}",
                options=[  # Business month END
                    {"label": "None", "value": "None"},
                    {"label": "Monthly", "value": "BM"},
                    {"label": "Quarterly", "value": "BQ"},
                    {"label": "Annualy", "value": "BA"},
                    {"label": "Semi-Annualy", "value": "6BM"},
                ],
            ),
            html.Div(id=f"output-contribution-dpp-{id}"),
        ]
    )


def rebalancing_dates(id):
    return html.Div(
        [
            html.I("Rebalancing frequency"),
            html.Br(),
            dcc.Dropdown(
                id=f"rebalancing-dropdown-{id}",
                options=[  # Business month END
                    {"label": "None", "value": "None"},
                    {"label": "Monthly", "value": "BM"},
                    {"label": "Quarterly", "value": "BQ"},
                    {"label": "Annualy", "value": "BA"},
                    {"label": "Semi-Annualy", "value": "6BM"},
                ],
            ),
            html.Div(id=f"output-rebalancing-{id}"),
        ]
    )


def lazy_portfolios(id):
    return dcc.Dropdown(
        id=f"lazy-portfolios-{id}",
        placeholder="Lazy",
        className="has-text-left",
        options=[  # Business month END
            {"label": "None", "value": "None"},
            {"label": "Lazy 1", "value": "Lazy 1"},
            {"label": "Lazy 2", "value": "Lazy 2"},
            {"label": "Lazy 3", "value": "Lazy 3"},
            {"label": "Lazy 4", "value": "Lazy 4"},
        ],
    )


def portfolio_name(id):
    return html.Div(
        dcc.Input(
            placeholder=f"Portfolio {id}",
            type="text",
            value=f"Portfolio {id}",
            style={
                "border-width": "0px",
                "color": "#363636",
                "font-size": "2rem",
                "font-weight": "600",
                "line-height": "1.125",
                "padding-bottom": "0.5cm",
            },
            id=f"portfolio-name-{id}",
        ),
        className="column is-11 has-text-left",
    )


def options(id, visibility):
    return html.Div(
        [
            html.Div(
                [
                    portfolio_name(id),
                    html.Div(
                        lazy_portfolios(id), className="column is-1 has-text-right"
                    ),
                    html.Div(contribution_amount(id), className="column is-12"),
                    html.Div(contribution_dates(id), className="column is-12"),
                    html.Div(rebalancing_dates(id), className="column is-12"),
                    html.Div(ticker_selector(id), className="column is-12"),
                ],
                className="columns is-multiline",
            )
        ],
        className="box",
        id=f"portfolio-{id}",
        style={"display": f"{visibility}"},
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


def options_wrapper():
    return html.Div(
        [
            html.Div(
                [html.Div(select_dates()), html.Div(initial_amount_of_money())],
                className="box",
            ),
            html.Div(
                children=[
                    options(1, visibility="block"),
                    options(2, visibility="none"),
                    options(3, visibility="none"),
                    options(4, visibility="none"),
                    options(5, visibility="none"),
                ],
                id="portfolios-container",
            ),
            add_portfolio_button(),
            html.Br(),
            submit_button(),
        ],
        id="portfolios-main",
    )
