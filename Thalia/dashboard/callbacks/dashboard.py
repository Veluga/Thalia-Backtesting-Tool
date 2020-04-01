import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from decimal import Decimal
from datetime import datetime

from analyse_data import analyse_data as anda
from ..config import MAX_PORTFOLIOS, OFFICIAL_COLOURS, NO_TABS
from .summary import get_pie_charts, get_yearly_differences_graph
from ..strategy import get_strategy, get_table_data


def register_dashboard(dashapp):
    """
    Works as essentially react component routing.
    Whenever changes happen in an Input components chosen attribute
    function is called with Input and States as values and func
    returns values are sent to Output components
    """

    # Register sending portfolio data
    register_update_dashboard(dashapp)

    # Register tab switch upon submit
    register_tab_switch(dashapp)


def register_update_dashboard(dashapp):
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
            # Pie Chart
            Output(f"pie-{i}", "figure"),
            Output(f"graph-box-pie-{i}", "style"),
        ]

    dashapp.callback(outputs, [Input("submit-btn", "n_clicks")], states)(
        update_dashboard
    )


def register_tab_switch(dashapp):
    """
    On backtest submission: enable all tabs and switch the active tab to the summary page.
    """
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


def tab_switch(n_clicks, *args):
    if n_clicks is None or None in args:
        raise PreventUpdate

    return ["summary"] + [False] * (NO_TABS - 1)


def retrieve_args(args):
    def get_args(args, offset):
        """
        Returns offset-th element of arguments
        Needed to work around dynamic Dash elements
        """
        return [list(args)[i * 5 + offset] for i in range(MAX_PORTFOLIOS)]

    """
    For Regression Testing Parameter changes to Update_dashboard,
    Returns a Dictionary of parameters
    """
    args_dict = {}
    args_dict["Portfolio Names"] = get_args(args, offset=0)
    args_dict["Contribution Amounts"] = get_args(args, offset=1)
    args_dict["Contribution Frequencies"] = get_args(args, offset=2)
    args_dict["Rebalancing Frequencies"] = get_args(args, offset=3)
    args_dict["Ticker Tables"] = get_args(args, offset=4)
    return args_dict


def get_no_portfolios(args):
    """
    Return how many protfolios the user has sent on input,
    based on the first empty argument
    """
    if not args:
        return 0
    elif None in args:
        return args.index(None)
    else:
        return MAX_PORTFOLIOS


def validate_dates(start_date, end_date, frequency):
    """
    Validate the dates selected, return an empty set otherwise
    """
    if str(frequency) != "None":
        return pd.date_range(start_date, end_date, freq=frequency)
    else:
        return set()


def format_date(date):
    format_string = "%Y-%m-%d"
    return datetime.strptime(date, format_string)


def get_box_of_metrics(portfolio_name, strategy_object, key_metrics):
    """
    Returns portfolio name, Initial Balance, Final Balance, Best Year, Worst Year, and values in Best Year, Worst Year
    """
    box_metrics = [portfolio_name]
    box_metrics += [round(key_metrics[j]["value"], 1) for j in range(4)]
    box_metrics += [
        anda.best_year_no(strategy_object),
        anda.worst_year_no(strategy_object),
    ]
    return box_metrics


def hidden_divs_data(no_portfolios):
    """
    As Dash does not allow dynamically registered callbacks, we need to return values for the hidden divs,
    ie for the number of portfolios left empty
    Corresponds to:
        - Box Visibility
        - Portfolio Name
        - Initial Balance
        - End Balance
        - Best Year %
        - Worst Year %
        - Best Year
        - Worst Year
        - Annual Differences Graph
        - Pie Chart
        - Pie Chart Visibility
    """
    empty_divs = [
        {"display": "none"},
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        {"display": "none"},
    ]
    return empty_divs * (MAX_PORTFOLIOS - no_portfolios)


def get_figure(xaxis_title, yaxis_title):
    fig = go.Figure()
    fig.update_layout(
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"),
    )
    return fig


def get_trace(x, y, name, color):
    return go.Scattergl(x=x, y=y, mode="lines", name=name, marker_color=color)


def update_dashboard(n_clicks, start_date, end_date, input_money, *args):
    """
    Based on selected tickers and assets update the whole dashapp.

    *args is for all the specific portfolio data, which involves:
    - Portfolio Name
    - Contribution Amount
    - Contribution Frequency
    - Rebalancing Frequency
    - Table of Tickers

    The function updates:
    - The Main Portfolio Graph
    - Visibility for Portfolio Data
    - Box of Key Metrics per Portfolio
    - Yearly Differences Graph per Portfolio
    - Pie Charts of Asset Allocations per Portfolio
    - SOON: Table of Key Metrics
    """

    if n_clicks is None:
        raise PreventUpdate

    # Retrieve arguments, as they are combined for Dash
    args = retrieve_args(args)

    no_portfolios = get_no_portfolios(args["Ticker Tables"])

    # Prevent update if no portfolios were given
    values = (start_date, end_date, input_money)
    if None in values or no_portfolios == 0:
        raise PreventUpdate

    main_graph = get_figure(xaxis_title="Time", yaxis_title="Total Returns")
    to_return = []

    start_date = format_date(start_date)
    end_date = format_date(end_date)

    for i in range(no_portfolios):
        portfolio_name = args["Portfolio Names"][i]
        contribution_dates = validate_dates(
            start_date, end_date, args["Contribution Frequencies"][i]
        )
        contribution_amount = args["Contribution Amounts"][i] or 0
        rebalancing_dates = validate_dates(
            start_date, end_date, args["Rebalancing Frequencies"][i]
        )

        tickers, proportions = zip(
            *(
                (tkr["AssetTicker"], Decimal(tkr["Allocation"]))
                for tkr in args["Ticker Tables"][i]
            )
        )

        strategy = get_strategy(
            tickers,
            proportions,
            start_date,
            end_date,
            input_money,
            contribution_amount,
            contribution_dates,
            rebalancing_dates,
        )

        total_returns = anda.total_return(strategy)
        table_data = get_table_data(strategy, total_returns)

        # Add Portfolio Trace to Main Graph
        main_graph.add_trace(
            get_trace(
                total_returns.index,
                total_returns.tolist(),
                name=str(portfolio_name),
                color=OFFICIAL_COLOURS[i],
            )
        )

        # Visibility
        to_return.append({"display": "block"})

        # Box of Metrics
        to_return += get_box_of_metrics(portfolio_name, strategy, table_data)

        # Yearly Differences Graph
        annual_figure = get_yearly_differences_graph(
            portfolio_name,
            anda.relative_yearly_returns(strategy),
            strategy.dates[0],
            strategy.dates[-1],
        )
        to_return.append(annual_figure)

        # Pie Charts
        to_return += get_pie_charts(tickers, proportions)

    # Data for the hidden divs
    to_return += hidden_divs_data(no_portfolios)

    return [main_graph] + to_return
