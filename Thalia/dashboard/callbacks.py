import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import date
from decimal import Decimal

from analyse_data import analyse_data as anda


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


def update_backtest_results(tickers, proportions):
    """
    get timeseries and key metrics data for portfolio
    """
    # TODO: add error handling for ticker not found
    weights = [Decimal(p) for p in proportions]
    normalise(weights)

    start_date = date(2000, 1, 1)
    end_date = date(2010, 12, 31)

    assets_data = get_assets(tickers, weights, start_date, end_date)
    risk_free_rate = mock_risk_free(start_date, end_date)

    strategy = anda.Strategy(
        start_date,
        end_date,
        Decimal("10000.00"),
        assets_data,
        set(),
        Decimal("0.00"),
        set(),
    )
    table_data = get_table_data(strategy, risk_free_rate)
    returns = anda.total_return(strategy)
    return get_figure(returns), table_data


def get_table_data(strat, risk_free_rate=None):
    """
    return a list of key metrics and their values
    """
    returns = anda.total_return(strat)
    table = [
        {"metric": "Initial Balance", "value": returns[strat.dates[0]]},
        {"metric": "End Balance", "value": returns[strat.dates[-1]]},
        {"metric": "Best Year", "value": anda.best_year(strat)},
        {"metric": "Worst Year", "value": anda.worst_year(strat)},
        {"metric": "Max Drawdown", "value": anda.max_drawdown(strat)},
    ]
    if risk_free_rate is not None:
        try:
            # We can't use append here because we want the table
            # unaltered if anything goes wrong.
            table = table + [
                {
                    "metric": "Sortino Ratio",
                    "value": anda.sortino_ratio(strat, risk_free_rate),
                },
                {
                    "metric": "Sharpe Ratio",
                    "value": anda.sharpe_ratio(strat, risk_free_rate),
                },
            ]
        except Exception:
            print("Could not calculate Sharpe/Sortino ratios")

    return table


def get_figure(total_returns):
    fig = go.Figure()
    fig.add_trace(get_trace(total_returns.index, total_returns.tolist()))
    return fig


def get_trace(x, y):
    return go.Scatter(x=x, y=y, mode="lines+markers",)


def normalise(arr):
    """
    Changes arr in place, keeping the relative weights the same,
    but scaling it such that it totals to 1.
    """
    total = sum(arr)
    for i in range(len(arr)):  # We're mutating so we have to index horribly.
        arr[i] /= total


def get_assets(tickers, proportions, start_date, end_date):
    """
    Gets data for each ticker and puts it in an anda.Asset.
    Returns a list of all assets.
    """
    assert len(tickers) == len(proportions)
    return [
        anda.Asset(tick, prop, mock_prices(tick, start_date, end_date))
        for tick, prop in zip(tickers, proportions)
    ]


def mock_prices(ticker, start_date, end_date):
    """
    Makes up data and shoves it in a dataframe.
    """
    import numpy as np

    date_rng = pd.date_range(start=start_date, end=end_date, freq="D")
    columns = ["Open", "Low", "High", "Close"]

    n_rows = len(date_rng)
    n_cols = len(columns)
    prices = [[Decimal("5.00") for _ in range(n_cols)] for _ in range(n_rows)]

    df = pd.DataFrame(prices, index=date_rng, columns=columns)
    return df


def mock_risk_free(start_date, end_date):
    return mock_prices("TODO: actual US Bonds name", start_date, end_date)
