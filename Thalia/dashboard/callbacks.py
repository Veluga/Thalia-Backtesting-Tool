import pandas as pd
import plotly.graph_objects as go
import uuid
import multiprocessing
import time
import os
import base64
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from decimal import Decimal
from . import util
from datetime import datetime, timedelta

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
    # gets ticker data, pass tickers and proportions, runs backetesting,
    # passes result to figures graphs, tables
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
    # assets_data.extend(user_upload_data(thigns))

    real_start_date = max(asset.values.index[0] for asset in assets_data)
    real_end_date = min(asset.values.index[-1] for asset in assets_data)

    print(real_end_date - real_start_date)

    if real_end_date < real_start_date:
        # raise Error
        return None, None

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
        {"metric": "Max Drawdown", "value": anda.max_drawdown(strat)},
    ]
    try:
        # We can't use append here because we want the table
        # unaltered if anything goes wrong.
        table = table + [
            {"metric": "Best Year", "value": anda.best_year(strat)},
            {"metric": "Worst Year", "value": anda.worst_year(strat)},
        ]
        table = table + [
            {"metric": "Sortino Ratio", "value": anda.sortino_ratio(strat, None)},
            {"metric": "Sharpe Ratio", "value": anda.sharpe_ratio(strat, None)},
        ]
    except anda.InsufficientTimeframe:
        print("Not enough enough data for best/worst year")
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


USER_DATA_DIR = "Thalia/dashboard/user-data/"


def store_user_asset(encoded, timeout=timedelta(minutes=30)):
    """
    Takes the base64 representation of a user's custom uploaded data and
    stores it in a file. Returns a handle that can be passed to
    `retrieve_user_asset` to get the data back.
    The data will only be valid for a short time (~30 minutes), so
    retrieval may fail.
    Raises a ValueError if the data is not valid utf-8. (maybe?)
    """
    """
    The caller should treat the handle as an opaque type, but if you
    need to modify this code it is a tuple of (str, datetime)
    representing the filepath ("user-data/<uuid>.csv") and last-accessible moment.
    Soon after the last-accessible moment, a subprocess will delete the
    file.
    The files are stored in the directory `Thalia/dashboard/user-data/`.
    """
    decoded_bytes = base64.b64decode(encoded)
    identifier = uuid.uuid4()
    filepath = USER_DATA_DIR + str(identifier) + ".csv"
    end_time = datetime.now() + timeout

    with open(filepath, "w") as out_file:
        out_file.write(decoded_bytes.decode("utf-8"))

    # We want a bit of buffer time to avoid race conditions.
    delay_sec = int(timeout.total_seconds() * 1.2)
    deleter = multiprocessing.Process(
        target=wait_and_delete, args=(filepath, delay_sec)
    )
    deleter.start()

    return (filepath, end_time)


def retrieve_user_asset(handle):
    """
    Takes a handle returned by store_user_asset and returns dataframe
    that can be passed to anda.
    If the file doesn't exist, or has timed out, raises FileNotFoundError.
    If the data is invalid, carries the exception upward from anda's parser.
    """
    filepath, last_moment = handle
    if last_moment <= datetime.now():
        raise FileNotFoundError(f"{filepath} has timed out.")
    return anda.parse_csv(filepath)


def wait_and_delete(filepath, delay_sec):
    # TODO: Security audit.
    assert USER_DATA_DIR == filepath[: len(USER_DATA_DIR)]
    assert ".." not in filepath
    assert "~" not in filepath
    assert "//" not in filepath
    time.sleep(delay_sec)
    os.remove(filepath)
