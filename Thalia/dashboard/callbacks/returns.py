from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
from ..config import MAX_PORTFOLIOS
from ..config import OFFICIAL_COLOURS
import dash_html_components as html

import pandas as pd
import dash_table
import sys


def register_return_tab(dashapp):
    register_print_dates(dashapp)
    # register_returns_table(dashapp)


def register_print_dates(dashapp):
    """ Callback for showing dates on summary tab """
    dashapp.callback(
        Output("output-date", "children"),
        [Input("submit-btn", "n_clicks")],
        [
            State("my-date-picker-range", "start_date"),
            State("my-date-picker-range", "end_date"),
        ],
    )(print_dates)


def update_table(name, diffs, start_date, end_date):
    test_diffs = pd.DataFrame(diffs)
    columns = [{"name": "metric", "id": "metric"}, {"name": "value", "id": "value"}]
    # data = (test_diffs.to_dict("rows"),)
    # columns = []
    data = [{"metric": "DUDVN", "value": " ege"}]
    annual_figure = dash_table.DataTable(data=data, columns=columns)

    return annual_figure


def print_dates(n_clicks, start_date, end_date):
    if n_clicks is None:
        raise PreventUpdate

    return f"Selected interval: {start_date} - {end_date}"
