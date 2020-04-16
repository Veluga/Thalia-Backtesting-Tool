import json

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from .. import user_csv
from ..config import MAX_PORTFOLIOS


def register_allocations_tab(dashapp):
    register_table_callbacks(dashapp)
    register_add_portfolio(dashapp)
    register_warning_csv(dashapp)
    register_user_data(dashapp)
    register_warning_message(dashapp)
    register_warning_date_csv(dashapp)


def register_table_callbacks(dashapp):
    """ Callback tying the ticker dropdown to table """
    for i in range(1, MAX_PORTFOLIOS + 1):
        dashapp.callback(
            Output(f"memory-table-{i}", "data"),
            [
                Input(f"memory-ticker-{i}", "value"),
                Input(f"output-data-upload-{i}", "children"),
                Input(f"lazy-portfolios-{i}", "value"),
            ],
            [State(f"memory-table-{i}", "data")],
        )(filter_tickers)


def register_user_data(dashapp):
    for i in range(1, MAX_PORTFOLIOS + 1):
        dashapp.callback(
            Output(f"output-data-upload-{i}", "children"),
            [Input(f"upload-data-{i}", "contents")],
            [State(f"upload-data-{i}", "filename")],
        )(update_output)


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


def register_warning_csv(dashapp):
    for i in range(1, MAX_PORTFOLIOS + 1):
        dashapp.callback(
            Output(f"confirm-csv-{i}", "displayed"),
            [Input(f"upload-data-{i}", "contents")],
        )(user_csv_warning)


def register_warning_date_csv(dashapp):
    for i in range(1, MAX_PORTFOLIOS + 1):
        dashapp.callback(
            Output(f"confirm-csv-date-{i}", "displayed"),
            [Input(f"upload-data-{i}", "contents")],
        )(user_csv_date_warning)


def warning_message(n_clicks, start_date, end_date, input_money, table):
    values = (start_date, end_date, input_money, table)
    if n_clicks:
        return not all(values)


def filter_tickers(ticker_selected, user_supplied_csv, lazy_portfolio, param_state):
    """
    Filters the selected tickers from the dropdown menu.
    """

    if (ticker_selected or lazy_portfolio or user_supplied_csv) is None:
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
        if ticker_selected is None:
            filename = user_supplied_csv[0]
            handle = user_supplied_csv[1]
            asset = {
                "AssetTicker": filename,
                "Handle": handle,
                "Allocation": "0",
            }
        else:
            ticker, name = ticker_selected.split(" – ")
            asset = {"AssetTicker": ticker, "Name": name, "Allocation": "0"}

        if all(
            asset["AssetTicker"] != existing["AssetTicker"] for existing in param_state
        ):
            param_state.append(asset)

    return param_state


def user_csv_warning(contents):
    if contents is not None:
        content_type, content_string = contents.split(",")
        try:
            user_csv.store(content_string)
        except user_csv.FormattingError:
            return True


def user_csv_date_warning(contents):
    if contents is not None:
        content_type, content_string = contents.split(",")
        try:
            user_csv.store_checked(content_string)
        except user_csv.anda.InsufficientTimeframe:
            return True


def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [user_data(list_of_contents, list_of_names)]
        return children[0]


def user_data(contents, filename):
    content_type, content_string = contents.split(",")
    try:
        handle = user_csv.store(content_string)
    except user_csv.FormattingError:
        raise PreventUpdate
    try:
        handle = user_csv.store_checked(content_string)
    except user_csv.anda.InsufficientTimeframe:
        raise PreventUpdate
    return [filename, handle]


def add_portfolio(n_clicks, *args):
    """
    Makes input fields for another portfolio visible.
    If the number of portfolios has reached MAX_PORTFOLIOS, no update.
    """
    if n_clicks is None or n_clicks >= MAX_PORTFOLIOS:
        raise PreventUpdate

    no_portfolios = n_clicks

    ret = list(args)
    ret[no_portfolios] = {"display": "block"}
    if no_portfolios < MAX_PORTFOLIOS - 1:
        return ret + [False]
    else:
        return ret + [True]
