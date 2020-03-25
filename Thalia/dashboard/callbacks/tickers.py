from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from ..config import MAX_PORTFOLIOS


def register_tickers_tab(dashapp):
    register_table_callbacks(dashapp)
    register_add_portfolio(dashapp)


def register_table_callbacks(dashapp):
    """ Callback tying the ticker dropdown to table """
    for i in range(1, MAX_PORTFOLIOS + 1):
        dashapp.callback(
            Output(f"memory-table-{i}", "data"),
            [Input(f"memory-ticker-{i}", "value")],
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
        return ret + [False]
    else:
        return ret + [True]
