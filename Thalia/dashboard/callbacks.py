import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from decimal import Decimal
from . import util
from datetime import datetime

from analyse_data import analyse_data as anda


MAX_PORTFOLIOS = 5
OFFICIAL_COLOURS = [
    "#f26a4b",
    "#01434a",
    "#01191c",
    "#f23d3d",
    "#feedd0",
]


def register_dashboard(dashapp):
    """ Main callback, instantiates strategy object """
    # Backtest constraints
    states = [
        State("my-date-picker-range", "start_date"),
        State("my-date-picker-range", "end_date"),
        State("input-money", "value"),
    ]

    # Portfolio Growth Graph
    outputs = [Output(f"main-graph", "figure")]
    for i in range(1, MAX_PORTFOLIOS + 1):

        # Portfolio specific data
        states += [
            State(f"portfolio-name-{i}", "value"),
            State(f"input-contribution-{i}", "value"),
            State(f"contribution-dropdown-{i}", "value"),
            State(f"rebalancing-dropdown-{i}", "value"),
            State(f"memory-table-{i}", "data"),
        ]

        # Portfolio specific out
        outputs += [
            # Box visibility
            Output(f"metrics-box-{i}", "style"),
            # Box data
            Output(f"box-Portfolio Name-{i}", "children"),
            Output(f"box-Initial Investment-{i}", "children"),
            Output(f"box-End Balance-{i}", "children"),
            Output(f"box-Difference in Best Year-{i}", "children"),
            Output(f"box-Difference in Worst Year-{i}", "children"),
            Output(f"box-Best Year-{i}", "children"),
            Output(f"box-Worst Year-{i}", "children"),
            # Annual returns graph
            Output(f"annual-returns-{i}", "figure"),
        ]

    dashapp.callback(outputs, [Input("submit-btn", "n_clicks")], states)(
        update_dashboard
    )


def register_table_callbacks(dashapp):
    """ Callback tying the ticker dropdown to table """
    for i in range(1, MAX_PORTFOLIOS + 1):
        dashapp.callback(
            Output(f"memory-table-{i}", "data"),
            [Input(f"memory-ticker-{i}", "value")],
            [State(f"memory-table-{i}", "data")],
        )(filter_tickers)


def register_tab_switch(dashapp):
    """ Callback for switching and enabling tabs """
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
        [
            State("my-date-picker-range", "start_date"),
            State("my-date-picker-range", "end_date"),
            State("input-money", "value"),
            State("memory-table-1", "data"),
        ],
    )(tab_switch)


def register_add_portfolio_button(dashapp):
    """ Callback for adding new portfolios and disabling button at 5 """
    dashapp.callback(
        [Output(f"portfolio-{i}", "style") for i in range(1, MAX_PORTFOLIOS + 1)]
        + [Output("add-portfolio-btn", "disabled")],
        [Input("add-portfolio-btn", "n_clicks")],
        [State(f"portfolio-{i}", "style") for i in range(1, MAX_PORTFOLIOS + 1)],
    )(add_portfolio)


def register_pie_charts(dashapp):
    """ Callback for the piecharts per portfolio """
    dashapp.callback(
        [
            item
            for i in range(1, MAX_PORTFOLIOS + 1)
            for item in (
                Output(f"pie-{i}", "figure"),
                Output(f"graph-box-pie-{i}", "style"),
            )
        ],
        [Input("submit-btn", "n_clicks")],
        [State(f"memory-table-{i}", "data") for i in range(1, MAX_PORTFOLIOS + 1)],
    )(pie_charts)


def register_asset_contributions_table(dashapp):
    dashapp.callback(
        [
            Output(f"asset-contributions-{i}", "data")
            for i in range(1, MAX_PORTFOLIOS + 1)
        ],
        [Input("submit-btn", "n_clicks")],
        [State(f"memory-table-{i}", "data") for i in range(1, MAX_PORTFOLIOS + 1)],
    )(asset_contributions_table)


def register_callbacks(dashapp):
    """
    Works as essentially react component routing.
    Whenever changes happen in an Input components chosen attribute
    function is called with Input and States as values and func
    returns values are sent to Output components
    """

    # Register sending portfolio data
    register_dashboard(dashapp)

    # Register updating the tables with the ticker dropdown
    register_table_callbacks(dashapp)

    # Register tab switch upon submit
    register_tab_switch(dashapp)

    # Register add Portfolio Button
    register_add_portfolio_button(dashapp)

    # Register plotting asset distribution
    register_pie_charts(dashapp)

    # Register contributions per assets
    # register_asset_contributions_table(dashapp)


def asset_contributions_table(n_clicks, *args):
    # TODO
    if n_clicks is None:
        raise PreventUpdate

    if None in args:
        no_portfolios = args.index(None)
    else:
        no_portfolios = 5

    ret = []
    for i in range(no_portfolios):
        ret.append(args[i])

    for i in range(no_portfolios, MAX_PORTFOLIOS):
        ret.append(None)

    return ret


def pie_charts(n_clicks, *args):
    if n_clicks is None:
        raise PreventUpdate

    if None in args:
        no_portfolios = args.index(None)
    else:
        no_portfolios = 5

    ret = []
    for i in range(no_portfolios):
        tickers, proportions = zip(
            *((tkr["AssetTicker"], Decimal(tkr["Allocation"])) for tkr in args[i])
        )
        fig = go.Figure(data=[go.Pie(labels=tickers, values=proportions)])
        fig.update_traces(hoverinfo="label", marker=dict(colors=OFFICIAL_COLOURS))
        ret += [fig, {"display": "block"}]

    for i in range(no_portfolios, MAX_PORTFOLIOS):
        ret += [None, {"display": "none"}]

    return ret


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


def add_portfolio(n_clicks, *args):
    if n_clicks is None or n_clicks >= MAX_PORTFOLIOS:
        raise PreventUpdate
    no_portfolios = n_clicks

    ret = list(args)
    ret[no_portfolios] = {"display": "block"}
    if no_portfolios < MAX_PORTFOLIOS - 1:
        ret.append(False)
    else:
        ret.append(True)
    return ret


def tab_switch(n_clicks, *args):
    if n_clicks is None or None in args:
        raise PreventUpdate

    return "summary", False, False, False, False, False


def update_dashboard(n_clicks, start_date, end_date, input_money, *args):
    """
    based on selected tickers and assets generate a graph of portfolios value over time
    and a table of key metrics
    """

    if n_clicks is None:
        raise PreventUpdate

    portfolio_name_args = [list(args)[i * 5] for i in range(MAX_PORTFOLIOS)]
    contribution_amount_args = [list(args)[i * 5 + 1] for i in range(MAX_PORTFOLIOS)]
    contribution_frequency_args = [list(args)[i * 5 + 2] for i in range(MAX_PORTFOLIOS)]
    rebalancing_frequency_args = [list(args)[i * 5 + 3] for i in range(MAX_PORTFOLIOS)]
    table_data_args = [list(args)[i * 5 + 4] for i in range(MAX_PORTFOLIOS)]

    if None in table_data_args:
        no_portfolios = table_data_args.index(None)
    else:
        no_portfolios = 5

    values = (start_date, end_date, input_money)
    if None in values or no_portfolios == 0:
        raise PreventUpdate

    fig = get_figure()
    return_key_metrics = []

    format_string = "%Y-%m-%d"
    start_date = datetime.strptime(start_date, format_string)
    end_date = datetime.strptime(end_date, format_string)

    for i in range(no_portfolios):
        if str(contribution_frequency_args[i]) != "None":
            contribution_dates = pd.date_range(
                start_date, end_date, freq=contribution_frequency_args[i]
            )
        else:
            contribution_dates = set()
        if str(rebalancing_frequency_args[i]) != "None":
            rebalancing_dates = pd.date_range(
                start_date, end_date, freq=rebalancing_frequency_args[i]
            )
        else:
            rebalancing_dates = set()
        if contribution_amount_args[i] is None:
            contribution_amount_args[i] = 0

        tickers, proportions = zip(
            *(
                (tkr["AssetTicker"], Decimal(tkr["Allocation"]))
                for tkr in table_data_args[i]
            )
        )

        total_returns, key_metrics = update_backtest_results(
            tickers,
            proportions,
            start_date,
            end_date,
            input_money,
            contribution_amount_args[i],
            contribution_dates,
            rebalancing_dates,
        )

        fig.add_trace(
            get_trace(
                total_returns.index,
                total_returns.tolist(),
                name=str(portfolio_name_args[i]),
                color=OFFICIAL_COLOURS[i],
            )
        )

        return_key_metrics += [{"display": "block"}, portfolio_name_args[i]]
        return_key_metrics += [round(key_metrics[j]["value"], 1) for j in range(4)]
        return_key_metrics += ["1", "2"]  # TODO Add date for best and worst year here

        # TODO add annual returns here
        annual_figure = go.Figure(
            data=[
                go.Bar(
                    name="SF Zoo", x=["zebras", "gorillas", "monkeys"], y=[20, 14, 23]
                ),
            ]
        )
        return_key_metrics.append(annual_figure)

    no_data = [{"display": "none"}, "", "", "", "", "", "", "", None]
    for i in range(no_portfolios, MAX_PORTFOLIOS):
        return_key_metrics += no_data

    return [fig] + return_key_metrics


def update_backtest_results(
    tickers,
    proportions,
    start_date,
    end_date,
    input_money,
    contribution_amount,
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
        contribution_amount,
        rebalancing_dates,
    )
    table_data = get_table_data(strategy)
    returns = anda.total_return(strategy)
    return returns, table_data


def get_table_data(strat):
    """
    return a list of key metrics and their values
    """
    returns = anda.total_return(strat)
    table = [
        {"metric": "Initial Balance", "value": returns[strat.dates[0]]},
        {"metric": "End Balance", "value": returns[strat.dates[-1]]},
    ]
    try:
        # We can't use append here because we want the table
        # unaltered if anything goes wrong.
        table = table + [
            {"metric": "Best Year", "value": anda.best_year(strat)},
            {"metric": "Worst Year", "value": anda.worst_year(strat)},
            {"metric": "Max Drawdown", "value": anda.max_drawdown(strat)},
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


def get_figure():
    fig = go.Figure()
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Total Returns",
        font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"),
    )
    return fig


def get_trace(x, y, name, color):
    return go.Scattergl(x=x, y=y, mode="lines", name=name, marker_color=color)


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
