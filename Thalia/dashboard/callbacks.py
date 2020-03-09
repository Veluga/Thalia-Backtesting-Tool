import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from decimal import Decimal
from .tab_elements.tickers import df
from datetime import datetime

from analyse_data import analyse_data as anda


MAX_PORTFOLIOS = 5
MAX_ASSETS = 15


def portfolio_states():
    states = [
        State("my-date-picker-range", "start_date"),
        State("my-date-picker-range", "end_date"),
        State("input-money", "value"),
    ]
    for i in range(1, MAX_PORTFOLIOS + 1):
        states += [
            State(f"input-contribution-{i}", "value"),
            State(f"contribution-dropdown-{i}", "value"),
            State(f"rebalancing-dropdown-{i}", "value"),
        ]

        for j in range(1, MAX_ASSETS + 1):
            states += [
                State(f"ticker-{i}-{j}", "value"),
                State(f"proportion-{i}-{j}", "value"),
            ]
    return states


def register_add_asset_buttons(dashapp):
    for i in range(1, MAX_PORTFOLIOS + 1):
        # Add Asset Button
        dashapp.callback(
            [
                Output(f"tickers-container-{i}", "children"),
                Output(f"add-asset-btn-{i}", "disabled"),
            ],
            [Input(f"add-asset-btn-{i}", "n_clicks")],
            [
                State(f"tickers-container-{i}", "children"),
                State(f"tickers-container-{i}", "id"),
            ],
        )(add_ticker)


def print_output(start_date, end_date):
    display_date = ("start date: ", start_date, " end date :", end_date)
    return display_date


def filter_tickers(tickers_selected, param_state):
    """
    Filters the selected tickers from the dropdown menu
    """
    if tickers_selected is None:
        raise PreventUpdate
    if param_state is None:
        param_state = []
    #  prefix variable name with @ to perform query
    filtered = df.query("AssetTicker in @tickers_selected")
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
        portfolio_states(),
    )(update_dashboard)

    # callback for add assets
    register_add_asset_buttons(dashapp)

    # pass input dates
    dashapp.callback(
        Output("output_dates", "children"),
        [
            Input("my-date-picker-range", "start_date"),
            Input("my-date-picker-range", "end_date"),
        ],
    )(print_output)

    # Tab switch upon submit
    dashapp.callback(
        [
            Output("tabs", "value"),
            Output("summary", "disabled"),
            Output("metrics", "disabled"),
            Output("returns", "disabled"),
            Output("drawdowns", "disabled"),
            Output("assets", "disabled"),
        ],
        [Input("submit-btn", "n_clicks")],
    )(tab_switch)

    # Add Portfolio Button
    dashapp.callback(
        Output("portfolios-container", "children"),
        [Input("add-portfolio-btn", "n_clicks")],
        [State("portfolios-container", "children")],
    )(add_portfolio)

    # Make button dissappear at 5 portfolios
    dashapp.callback(
        Output("add-portfolio-btn", "disabled"),
        [Input("add-portfolio-btn", "n_clicks")],
        [State("portfolios-container", "children")],
    )(remove_button)


def add_ticker(n_clicks, param_state, param_id):
    from .tab_elements.tickers import ticker_selector

    if n_clicks is None:
        raise PreventUpdate

    no_tickers = len(param_state)

    if no_tickers == MAX_ASSETS - 1:
        return param_state, True

    else:
        return param_state + [ticker_selector(param_id, no_tickers + 1)], False


def remove_button(n_clicks, param_state):
    if n_clicks is None:
        raise PreventUpdate

    no_portfolios = len(param_state)
    if no_portfolios < MAX_PORTFOLIOS - 1:
        raise PreventUpdate

    return True


def add_portfolio(n_clicks, param_state):
    from .tab_elements.tickers import options

    if n_clicks is None:
        raise PreventUpdate
    no_portfolios = len(param_state)
    return param_state + [options(no_portfolios + 1)]


def tab_switch(n_clicks):
    if n_clicks is None:
        raise PreventUpdate

    return "summary", False, False, False, False, False


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
    risk_free_rate = mock_risk_free(start_date, end_date)

    strategy = anda.Strategy(
        start_date,
        end_date,
        input_money,
        assets_data,
        contribution_dates,
        input_contribution,
        rebalancing_dates,
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
