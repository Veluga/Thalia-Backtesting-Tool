from datetime import datetime as dt

import pandas_datareader as pdr
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from . import layout


def create_time_series(dff, title, x, y):
    return dict(x=x, y=y, mode="lines+markers", name=title)


def get_data(tickers):
    return pdr.get_data_yahoo(tickers, start=dt(2017, 1, 1), end=dt.now())


def register_callbacks(dashapp):
    @dashapp.callback(
        Output("graph-container", "children"),
        [Input("submit-btn", "n_clicks")],
        [
            State("ticker1", "value"),
            State("ticker2", "value"),
            State("ticker3", "value"),
            State("ticker1-proportion", "value"),
            State("ticker2-proportion", "value"),
            State("ticker3-proportion", "value"),
        ],
    )
    def update_dashboard(
        n_clicks, ticker1, ticker2, ticker3, ticker1_prop, ticker2_prop, ticker3_prop
    ):
        if n_clicks is None:
            raise PreventUpdate
        tickers = [dropdown for dropdown in (ticker1, ticker2, ticker3) if dropdown]
        dfs = [get_data(ticker) for ticker in tickers]
        table_data = get_table_data()
        table_columns = [{"name": i, "id": i} for i in table_data[0].keys()]
        return [
            layout.create_graph(get_figure_data(tickers, dfs), "graph"),
            layout.create_table(table_data, table_columns, "table"),
        ]


def get_table_data():
    return [
        {"metric": "Initial Balance", "value": 100},
        {"metric": "End Balance", "value": 120},
        {"metric": "Best Year", "value": 0.141},
        {"metric": "Worst Year", "value": 0.141},
        {"metric": "Sortino Ratio", "value": 176.158},
        {"metric": "Sharpe Ratio", "value": 0.0057},
        {"metric": "Max Drawdown", "value": 24.944},
    ]


def get_figure_data(tickers, dfs):
    traces = [
        create_time_series(df, name, df.index, df.Close)
        for name, df in zip(tickers, dfs)
    ]
    figure = {
        "data": traces,
        "layout": {"margin": {"l": 40, "r": 0, "t": 20, "b": 30}},
    }
    return figure
