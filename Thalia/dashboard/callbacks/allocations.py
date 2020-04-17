import json
from datetime import datetime

import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from .. import user_csv
from ..config import MAX_PORTFOLIOS
from ..portfolio_manager import get_portfolios_list, retrieve_portfolio, store_portfolio
from ..strategy import normalise


def register_allocations_tab(dashapp):
    register_table_callbacks(dashapp)
    register_add_portfolio(dashapp)
    register_user_data(dashapp)
    register_warning_message(dashapp)

    register_save_portfolio(dashapp)
    register_list_portfolios(dashapp)
    register_url_reading(dashapp)


def register_url_reading(dashapp):
    dashapp.callback(
        Output("stored-portfolios-1", "value"), [Input("page-location-url", "pathname")]
    )(load_shared_portfolio)


def load_shared_portfolio(path):
    if path is None:
        raise PreventUpdate

    porto_id = path.rsplit("/", 1)[1]
    try:
        porto_id = int(porto_id)
    except ValueError:
        raise PreventUpdate

    return porto_id


def register_table_callbacks(dashapp):
    """ Callback tying the ticker dropdown to table """
    for i in range(1, MAX_PORTFOLIOS + 1):
        dashapp.callback(
            [
                Output(f"memory-table-{i}", "data"),
                Output(f"portfolio-name-{i}", "value"),
            ],
            [
                Input(f"memory-ticker-{i}", "value"),
                Input(f"output-data-upload-{i}", "children"),
                Input(f"lazy-portfolios-{i}", "value"),
                Input(f"stored-portfolios-{i}", "value"),
            ],
            [State(f"memory-table-{i}", "data")],
        )(add_ticker)


def register_save_portfolio(dashapp):
    for i in range(1, MAX_PORTFOLIOS + 1):
        dashapp.callback(
            [
                Output(f"save-portfolio-success-{i}", "children"),
                Output(f"save-portfolio-success-{i}", "className"),
            ],
            [Input(f"save-portfolio-{i}", "n_clicks")],
            [
                State("my-date-picker-range", "start_date"),
                State("my-date-picker-range", "end_date"),
                State("input-money", "value"),
                State(f"portfolio-name-{i}", "value"),
                State(f"memory-table-{i}", "data"),
            ],
        )(save_portfolio)


def register_list_portfolios(dashapp):
    dashapp.callback(
        [
            Output(f"stored-portfolios-{i}", "options")
            for i in range(1, MAX_PORTFOLIOS + 1)
        ],
        [
            Input(f"save-portfolio-success-{i}", "children")
            for i in range(1, MAX_PORTFOLIOS + 1)
        ]
        + [Input("page-location-url", "href")],
    )(list_stored_portfolios)


def list_stored_portfolios(*_):
    portfolios = get_portfolios_list()
    options = [{"label": name, "value": pid} for pid, name in portfolios]
    return [options] * MAX_PORTFOLIOS


def load_stored_portfolio(portfolio_id):
    porto, strat = retrieve_portfolio(portfolio_id)
    assets = []
    for tkr in strat.assets:
        ticker, name = tkr.ticker.split("|")
        assets.append({"AssetTicker": ticker, "Name": name, "Allocation": tkr.weight})
    return assets, porto.name


def save_portfolio(n_clicks, start_date, end_date, input_money, name, table_data):
    if n_clicks is None:
        raise PreventUpdate

    if not table_data or any(tkr["Allocation"] == 0 for tkr in table_data):
        raise PreventUpdate

    if any(tkr.get("Handle") for tkr in table_data):
        message = (
            f"You can not save portfolios with your own uploaded assets,"
            " please remove the asset before saving"
        )
        notification_type = "notification is-warning"
        return message, notification_type

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    allocations = [tkr["Allocation"] for tkr in table_data]
    normalise(allocations)
    tickers = (f"{tkr['AssetTicker']}|{tkr['Name']}" for tkr in table_data)

    success = store_portfolio(
        start_date, end_date, input_money, name, zip(tickers, allocations)
    )
    if success:
        message = f"Portfolio {name} saved"
        notification_type = "notification is-success"
    else:
        message = (
            f"You already have a portfolio called {name},"
            " please rename the portfolio and try again"
        )
        notification_type = "notification is-warning"

    return message, notification_type


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


def warning_message(n_clicks, start_date, end_date, input_money, table):
    values = (start_date, end_date, input_money, table)
    if n_clicks:
        return not all(values)


def add_ticker(
    ticker_selected, user_supplied_csv, lazy_portfolio, saved_portfolio, table_data
):
    """
    Filters the selected tickers from the dropdown menu.
    """
    if (
        ticker_selected or lazy_portfolio or user_supplied_csv or saved_portfolio
    ) is None:
        raise PreventUpdate

    if table_data is None:
        table_data = []
    portfolio_name = dash.no_update  # only update the name when loading a portfolio

    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    else:
        trigger = ctx.triggered[0]["prop_id"].split(".")[0]

    # load complete portfolio
    if trigger.startswith("stored-portfolios"):
        table_data, portfolio_name = load_stored_portfolio(saved_portfolio)

    elif trigger.startswith("lazy-portfolios"):
        table_data = list(json.loads(lazy_portfolio).values())

    # load single asset
    else:
        if trigger.startswith("output-data-upload"):
            filename = user_supplied_csv[0]
            handle = user_supplied_csv[1]
            asset = {
                "AssetTicker": filename,
                "Handle": handle,
                "Allocation": "0",
            }

        else:
            ticker, name = ticker_selected.split(" – ")
            asset = {"AssetTicker": ticker, "Name": name, "Allocation": 0}

        if all(
            asset["AssetTicker"] != existing["AssetTicker"] for existing in table_data
        ):
            table_data.append(asset)

    return table_data, portfolio_name


def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [user_data(c, n) for c, n in zip(list_of_contents, list_of_names)]
        assert len(children) == 1
        return children[0]


def user_data(contents, filename):
    content_type, content_string = contents.split(",")
    handle = user_csv.store(content_string)
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
