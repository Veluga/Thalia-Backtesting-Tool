import dash_core_components as dcc
import dash_html_components as html
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
                                {"name": i, "id": i, "editable": (i == "Allocation")}
                                for i in df.columns
                            ],
                            editable=True,
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
            dcc.DatePickerRange(
                id="my-date-picker-range",
                # max_date_allowed=dt.now()
                # initial_visible_month=dt(2017, 8, 5),
                # end_date=dt(2017, 8, 25)
            ),
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
                placeholder="Insert Initial amount of $",
                type="number",
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
                
            ),
             html.Label("Contribution frequency", className="label"),
            html.Div(id="output_contribution"),
            dcc.Dropdown(
                id="Contribution_dropdown",
                options=[
                    {"label": "Monthly", "value": "month"},
                    {"label": "Quarterly", "value": "quarter"},
                    {"label": "Annualy", "value": "year"},
                ],
            ),
        ]
    )


def options():
    return html.Div(
        [
            html.Div([select_dates()], className="container",),
            html.Div([initial_amount_of_money()], className="container",),
            html.Div([contribution_amount()], className="container",),
            html.Div([ticker_selector()], className="container",),
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
