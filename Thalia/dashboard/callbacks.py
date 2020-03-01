import pandas as pd
import sys
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import date
from decimal import Decimal
from . import layout
from datetime import datetime

from analyse_data import analyse_data as anda


def print_output(start_date, end_date):
    display_date = ("start date: ", start_date, " end date :", end_date)
    return display_date


def print_inputs(value):
    return 'You have selected "{}"'.format(value)


def filter_tickers(tickers_selected, param_state):
    """
    Filters the selected tickers from the dropdown menu
    """
    if tickers_selected is None:
        raise PreventUpdate
    if param_state is None:
        param_state = []
    filtered = layout.df.query("AssetTicker in @tickers_selected")
    dict_ver = filtered.to_dict(orient="records")
    new_store = param_state + (dict_ver)

    return new_store


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
    dashapp.callback(
        Output("output_contribution_dpp", "children"),
        [Input("contribution_dropdown", "value")],
    )(print_inputs)
    dashapp.callback(
        Output("output_money", "children"), [Input("input_money", "value")]
    )(print_inputs)
    dashapp.callback(
        Output("output_contribution", "children"),
        [Input("input_contribution", "value")],
    )(print_inputs)
    dashapp.callback(
        Output("output_rebalancing", "children"),
        [Input("rebalancing_dropdown", "value")],
    )(print_inputs)


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
    TODO: make proportion selection matter
    """
    # proportions_selected = (proportions_selected["Allocation"])
    # proportions_selected

    if n_clicks is None:
        raise PreventUpdate

    values = (
        tickers_selected,
        start_date,
        end_date,
        input_money,
        input_contribution,
        contribution_dropdown,
        rebalancing_dropdown,
    )
    if any(param is None for param in values):
        raise PreventUpdate
    if contribution_dropdown == "month":
        contribution_dropdown = pd.date_range(start_date, end_date, freq="M")
    elif contribution_dropdown == "quarter":
        contribution_dropdown = pd.date_range(start_date, end_date, freq="3M")
    elif contribution_dropdown == "year":
        contribution_dropdown = pd.date_range(start_date, end_date, freq="12M")
    elif contribution_dropdown == "midyear":
        contribution_dropdown = pd.date_range(start_date, end_date, freq="6M")

    if rebalancing_dropdown == "month":
        rebalancing_dropdown = pd.date_range(start_date, end_date, freq="M")
    elif rebalancing_dropdown == "quarter":
        rebalancing_dropdown = pd.date_range(start_date, end_date, freq="3M")
    elif rebalancing_dropdown == "year":
        rebalancing_dropdown = pd.date_range(start_date, end_date, freq="12M")
    elif rebalancing_dropdown == "midyear":
        rebalancing_dropdown = pd.date_range(start_date, end_date, freq="6M")
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
        contribution_dropdown,
        rebalancing_dropdown,
    )


def update_backtest_results(
    tickers,
    proportions,
    start_date,
    end_date,
    input_money,
    input_contribution,
    contribution_dropdown,
    rebalancing_dropdown,
):
    """
    get timeseries and key metrics data for portfolio
    """
    # TODO: add error handling for ticker not found
    print(proportions, file=sys.stdout)  # without explicit stdout printing did not work on windows
    weights = [p for p in proportions if p is not None]
    normalise(weights)


    assets_data = get_assets(tickers, weights, start_date, end_date)
    risk_free_rate = mock_risk_free(start_date, end_date)

    strategy = anda.Strategy(
        start_date,
        end_date,
        input_money,
        assets_data,
        contribution_dropdown,
        input_contribution,
        rebalancing_dropdown,
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
