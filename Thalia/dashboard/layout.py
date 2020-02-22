import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd

df = pd.DataFrame(
        [
            {"AssetTicker": "RCK", "Name": "Rock", "Allocation" : "0"},
            {"AssetTicker": "BRY", "Name": "Berry", "Allocation" : "0"},
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
                        html.Div([
                            dcc.Store(id="memory-output"),
                            dcc.Dropdown(id="memory_ticker", options=[
                            {'value': x, 'label': x} for x in AssetTicker],
                            multi = True,
                                        className="")],
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
                            id='memory-table',
                            columns=[{'name': i, 'id': i} for i in df.columns],
                            #data=data
                            editable=True,
                            row_deletable=True
                        )
                    ],
                    className='section'
                   )
             ),

            html.Div(
                html.Div(
                    [
                        html.Label("Allocation: ", className="label"),
                        html.Div(
                            dcc.Input(
                                id="proportion",
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
                [ticker_selector()],
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