import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


def register_callbacks(dashapp):
    """
    Works as essentially react component routing.
    Whenever changes happen in an Input components chosen attribute
    function is called with Input and States as values and func
    returns values are sent to Output components
    """
    dashapp.callback(
        [Output("graph", "figure"), Output("table", "data")],
        [Input("submit-btn", "n_clicks")],
        [
            State("ticker1", "value"),
            State("ticker2", "value"),
            State("ticker3", "value"),
            State("ticker1-proportion", "value"),
            State("ticker2-proportion", "value"),
            State("ticker3-proportion", "value"),
        ],
    )(update_dashboard)


# TODO: make input and output dynamic, currently only supports 3
# see this discussion for more info: https://community.plot.ly/t/dynamic-controls-and-dynamic-output-components/5519
# GOAL is to have the UI support selection and distribution of arbitary numbers of assets
def update_dashboard(
    n_clicks, ticker1, ticker2, ticker3, ticker1_prop, ticker2_prop, ticker3_prop
):
    """
    based on selected tickers and assets generate a graph of portfolios value over time
    and a table of key metrics

    TODO: make proportion selection matter
    """
    if n_clicks is None:
        raise PreventUpdate

    # TODO: add error handling (UI facing message) for erronous input
    all_tickers = (ticker1, ticker2, ticker3)
    all_proportions = (ticker1_prop, ticker2_prop, ticker3_prop)

    tickers, proportions = filter_dropdowns(all_tickers, all_proportions)
    return update_backtest_results(tickers, proportions)


def filter_dropdowns(tickers, proportions):
    """
    remove any ticker, proportion combos without a ticker selected

    TODO: maybe return a strategy object instead?
          currently does maybe a bit too much zipping and unzipping
    """
    tickers_with_prop = zip(tickers, proportions)
    tickers_with_prop = [
        dropdown for dropdown in tickers_with_prop if dropdown[0]
    ]  # remove empty dropdowns without a ticker
    tickers, proportions = zip(*tickers_with_prop)  # seperate tickers and props again
    return tickers, proportions


def update_backtest_results(tickers, proportion):
    """
    get timeseries and key metrics data for portfolio
    """
    # TODO: add error handling for ticker not found
    assets_data = get_data(tickers)
    # TODO: do anda stuff here
    table_data = get_table_data()
    return get_figure(assets_data), table_data


def get_table_data():
    """
    return a list of key metrics and their values

    TODO: add anda support here
    """
    return [
        {"metric": "Initial Balance", "value": 100},
        {"metric": "End Balance", "value": 120},
        {"metric": "Best Year", "value": 0.141},
        {"metric": "Worst Year", "value": 0.141},
        {"metric": "Sortino Ratio", "value": 176.158},
        {"metric": "Sharpe Ratio", "value": 0.0057},
        {"metric": "Max Drawdown", "value": 24.944},
    ]


def get_figure(df):
    fig = go.Figure()
    fig.add_trace(get_trace(df.index, df.data))
    return fig


def get_trace(x, y):
    return go.Scatter(x=x, y=y, mode="lines+markers",)


def get_data(ticker):
    """
    retrive ticker data from database

    TODO: add Finda support
    """
    import numpy as np

    date_rng = pd.date_range(start="1/1/2010", end="1/08/2010", freq="H")
    df = pd.DataFrame(date_rng, columns=["date"])
    df["data"] = np.random.randint(0, 100, size=(len(date_rng)))
    return df
