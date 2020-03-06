import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from decimal import Decimal
from . import layout
from datetime import datetime

from analyse_data import analyse_data as anda


def print_output(start_date, end_date):
    display_date = ("start date: ", start_date, " end date :", end_date)
    return display_date


def filter_tickers(ticker_selected, param_state):
    """
    Filters the selected tickers from the dropdown menu
    """
    if ticker_selected is None:
        raise PreventUpdate
    if param_state is None:
        param_state = []
    asset = {"AssetTicker": ticker_selected, "Allocation": "0"}
    if all(asset["AssetTicker"] != existing["AssetTicker"] for existing in param_state):
        param_state.append(asset)

    return param_state


def register_callbacks(dashapp):
    """
    Works as essentially react component routing.
    Whenever changes happen in an Input components chosen attribute
    function is called with Input and States as values and func
    returns values are sent to Output components
    """
    # gets ticker data, pass tickers and proportions, runs backetesting, passes result to figures graphs, tables
    dashapp.callback(
        [Output("graph", "figure"), Output("table", "data")],
        [Input("submit-btn", "n_clicks")],
        [
            State("memory-table", "data"),
            State("my-date-picker-range", "start_date"),
            State("my-date-picker-range", "end_date"),
            State("input_money", "value"),
            State("input_contribution", "value"),
            State("contribution_dropdown", "value"),
            State("rebalancing_dropdown", "value"),
        ],
    )(update_dashboard)

    # callback for updating the ticker table
    dashapp.callback(
        Output("memory-table", "data"),
        [Input("memory_ticker", "value")],
        [State("memory-table", "data")],
    )(filter_tickers)
    # pass input dates
    dashapp.callback(
        Output("output_dates", "children"),
        [
            Input("my-date-picker-range", "start_date"),
            Input("my-date-picker-range", "end_date"),
        ],
    )(print_output)


def update_dashboard(
    n_clicks,
    tickers_selected,
    start_date,
    end_date,
    input_money,
    input_contribution,
    contribution_dropdown,
    rebalancing_dropdown,
):
    """
    based on selected tickers and assets generate a graph of portfolios value over time
    and a table of key metrics
    """

    if n_clicks is None:
        raise PreventUpdate

    values = (
        tickers_selected,
        start_date,
        end_date,
        input_money,
    )
    if any(param is None for param in values):
        raise PreventUpdate
    if all(tkr["Allocation"] == 0 for tkr in tickers_selected):
        raise PreventUpdate

    if contribution_dropdown is not None:
        contribution_dates = pd.date_range(
            start_date, end_date, freq=contribution_dropdown
        )
    else:
        contribution_dates = set()
    if rebalancing_dropdown is not None:
        rebalancing_dates = pd.date_range(
            start_date, end_date, freq=rebalancing_dropdown
        )
    else:
        rebalancing_dates = set()
    if input_contribution is None:
        input_contribution = 0

    format_string = "%Y-%m-%d"
    start_date = datetime.strptime(start_date, format_string)
    end_date = datetime.strptime(end_date, format_string)
    tickers, proportions = zip(
        *((tkr["AssetTicker"], Decimal(tkr["Allocation"])) for tkr in tickers_selected)
    )

    return update_backtest_results(
        tickers,
        proportions,
        start_date,
        end_date,
        input_money,
        input_contribution,
        contribution_dates,
        rebalancing_dates,
    )


def update_backtest_results(
    tickers,
    proportions,
    start_date,
    end_date,
    input_money,
    input_contribution,
    contribution_dates,
    rebalancing_dates,
):
    """
    get timeseries and key metrics data for portfolio
    """
    # TODO: add error handling for ticker not found
    weights = [p for p in proportions if p is not None]
    normalise(weights)

    assets_data = get_assets(tickers, weights, start_date, end_date)

    real_start_date = min(asset.values.index[0] for asset in assets_data)
    real_end_date = max(asset.values.index[-1] for asset in assets_data)

    strategy = anda.Strategy(
        real_start_date,
        real_end_date,
        input_money,
        assets_data,
        contribution_dates,
        input_contribution,
        rebalancing_dates,
    )
    table_data = get_table_data(strategy)
    returns = anda.total_return(strategy)
    return get_figure(returns), table_data


def get_table_data(strat):
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
    try:
        # We can't use append here because we want the table
        # unaltered if anything goes wrong.
        table = table + [
            {
                "metric": "Sortino Ratio",
                "value": anda.sortino_ratio(strat, None),
            },
            {
                "metric": "Sharpe Ratio",
                "value": anda.sharpe_ratio(strat, None),
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
    return go.Scattergl(x=x, y=y, mode="lines+markers",)


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
    data = util.get_data(tickers, start_date, end_date)
    data = data.rename(
        columns={"AOpen": "Open", "AClose": "Close", "ALow": "Low", "AHigh": "High"}
    )
    assets = []
    for tick, prop in zip(tickers, proportions):
        asset_data = data[(data.AssetTicker == tick)]
        only_market_data = asset_data[["ADate", "Open", "Close", "Low", "High"]]
        only_market_data.index = only_market_data["ADate"]
        assets.append(anda.Asset(tick, prop, only_market_data))
    return assets

