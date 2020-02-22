import pandas as pd
from . import layout
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


def menu_callbacks(dashapp):
    dashapp.callback(
        Output('memory-output', 'data'),
        [Input('memory_ticker', 'value')])(filter_tickers)


def filter_tickers(tickers_selected):
    if not tickers_selected:
        # Return all the rows on initial load/no ticker selected.
        return layout.df.to_dict(orient='records')
    filtered = layout.df.query('AssetTicker in @tickers_selected')

    return filtered.to_dict(orient='records')


def table_callback(dashapp):
    dashapp.callback(Output('memory-table', 'data'),
              [Input('memory-output', 'data')])(on_data_set_table)


def on_data_set_table(data):
    if data is None:
        raise PreventUpdate

    return data


def dropdown_callback_table(dashapp):
    dashapp.callback(Output("memory_ticker", "value"), [Input("memory-table", "value")])
    (update_dropdown_if_delete)


def update_dropdown_if_delete(data):
    if data is None:
        raise PreventUpdate

    return data

# TODO: make input and output dynamic, currently only supports 3
# see this discussion for more info: https://community.plot.ly/t/dynamic-controls-and-dynamic-output-components/5519
# GOAL is to have the UI support selection and distribution of arbitary numbers of assets


def register_callbacks(dashapp):
    """
    Works as essentially react component routing.
    Whenever changes happen in an Input components chosen attribute
    function is called with Input and States as values and func
    returns values are sent to Output components
    """
    dashapp.callback(
        [Output("graph", "figure"), Output("table", "data")],
        [Input("submit-btn", "n_clicks"), Input("memory-table", "data"),
        Input("memory-table", "columns")]

    )(update_dashboard)


def update_dashboard(n_clicks, tickers_selected, proportions_selected):
    """
    based on selected tickers and assets generate a graph of portfolios value over time
    and a table of key metrics
    TODO: make proportion selection matter
    """
    if n_clicks is None:
        raise PreventUpdate

    # TODO: add error handling (UI facing message) for erronous input
    all_tickers = tickers_selected
    all_proportions = proportions_selected
    print(all_tickers, all_proportions)
    tickers, proportions = filter_dropdowns(all_tickers, all_proportions)
    return update_backtest_results(tickers, proportions)


def filter_dropdowns(tickers, proportions):
    """
    remove any ticker, proportion combos without a ticker selected
    TODO: maybe return a strategy object instead?
          currently does maybe a bit too much zipping and unzipping
    """
    tickers_with_prop = zip(tickers, proportions)
    tickers_with_prop = [
        dropdown for dropdown in tickers_with_prop if dropdown[0]
    ]  # remove empty dropdowns without a ticker
    tickers, proportions = zip(*tickers_with_prop)  # seperate tickers and props again
    return tickers, proportions


def update_backtest_results(tickers, proportion):
    """
    get timeseries and key metrics data for portfolio
    """
    # TODO: add error handling for ticker not found
    assets_data = get_data(tickers)
    # TODO: do anda stuff here
    table_data = get_table_data()
    return get_figure(assets_data), table_data


def get_table_data():
    """
    return a list of key metrics and their values
    TODO: add anda support here
    """
    return [
        {"metric": "Initial Balance", "value": 100},
        {"metric": "End Balance", "value": 120},
        {"metric": "Best Year", "value": 0.141},
        {"metric": "Worst Year", "value": 0.141},
        {"metric": "Sortino Ratio", "value": 176.158},
        {"metric": "Sharpe Ratio", "value": 0.0057},
        {"metric": "Max Drawdown", "value": 24.944},
    ]


def get_figure(df):
    fig = go.Figure()
    fig.add_trace(get_trace(df.index, df.data))
    return fig


def get_trace(x, y):
    return go.Scatter(x=x, y=y, mode="lines+markers",)


def get_data(ticker):
    """
    retrive ticker data from database
    TODO: add Finda support
    """
    import numpy as np

    date_rng = pd.date_range(start="1/1/2010", end="1/08/2010", freq="H")
    df = pd.DataFrame(date_rng, columns=["date"])
    df["data"] = np.random.randint(0, 100, size=(len(date_rng)))
    return df
    print(filter_tickers('RCK'))