from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import json

from ..config import MAX_PORTFOLIOS


def register_tickers_tab(dashapp):
    register_table_callbacks(dashapp)
    register_add_portfolio(dashapp)
    register_warning_message(dashapp)


def register_table_callbacks(dashapp):
    """ Callback tying the ticker dropdown to table """
    for i in range(1, MAX_PORTFOLIOS + 1):
        dashapp.callback(
            Output(f"memory-table-{i}", "data"),
            [
                Input(f"memory-ticker-{i}", "value"),
                Input(f"lazy-portfolios-{i}", "value"),
            ],
            [State(f"memory-table-{i}", "data")],
        )(filter_tickers)


def register_add_portfolio(dashapp):
    """ Callback for adding new portfolios and disabling button at 5 """
    dashapp.callback(
        [Output(f"portfolio-{i}", "style") for i in range(1, MAX_PORTFOLIOS + 1)]
        + [Output("add-portfolio-btn", "disabled")],
        [Input("add-portfolio-btn", "n_clicks")],
        [State(f"portfolio-{i}", "style") for i in range(1, MAX_PORTFOLIOS + 1)],
    )(add_portfolio)


def register_warning_message(dashapp):
    for i in range(1, MAX_PORTFOLIOS + 1):
        dashapp.callback(
            Output(f"confirm-{i}", "displayed"),
            [Input("submit-btn", "n_clicks")],
            [
                State("my-date-picker-range", "start_date"),
                State("my-date-picker-range", "end_date"),
                State("input-money", "value"),
                State(f"memory-table-{i}", "data"),
            ],
        )(warning_message)


def warning_message(n_clicks, start_date, end_date, input_money, table):
    values = (start_date, end_date, input_money, table)
    if n_clicks:
        return not all(values)


def filter_tickers(ticker_selected, lazy_portfolio, param_state):
    """
    Filters the selected tickers from the dropdown menu
    """

    if (ticker_selected or lazy_portfolio) is None:
        raise PreventUpdate
    if param_state is None:
        param_state = []
    if lazy_portfolio is not None:
        param_state = []
        json_acceptable_string = lazy_portfolio.replace("'", '"')
        lazy_dict = json.loads(json_acceptable_string)
        for asset in lazy_dict.values():
            if all(
                asset["AssetTicker"] != existing["AssetTicker"]
                for existing in param_state
            ):
                param_state.append(asset)
    else:
        ticker, name = ticker_selected.split(" – ")
        asset = {"AssetTicker": ticker, "Name": name, "Allocation": "0"}
        if all(
            asset["AssetTicker"] != existing["AssetTicker"] for existing in param_state
        ):
            param_state.append(asset)

    return param_state


def add_portfolio(n_clicks, *args):
    if n_clicks is None or n_clicks >= MAX_PORTFOLIOS:
        raise PreventUpdate

    no_portfolios = n_clicks

    ret = list(args)
    ret[no_portfolios] = {"display": "block"}
    if no_portfolios < MAX_PORTFOLIOS - 1:
        return ret + [False]
    else:
        return ret + [True]
