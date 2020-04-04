from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
from ..config import MAX_PORTFOLIOS
from ..config import OFFICIAL_COLOURS
import dash_html_components as html
import decimal
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


def get_data(name, diff, start_date, end_date):
    names = []
    diffs = []
    years = list(range(start_date.year + 1, end_date.year))
    diffs.append(diff)
    names.append(str(name))
    return [diffs, names, years]


def portfolios_figure(return_tab, no_portfolios):
    data_table = {}
    for i in range(0, no_portfolios):
        i = return_tab[i]
        name = i[1]
        diffs = i[0][0]

        data_table.update(
            {f"{str(name[0])}  returns": diffs.astype(float).round(2),}
        )

    df = pd.DataFrame(data_table).reset_index()

    df["index"] = df["index"].dt.strftime("%Y")
    print(df.columns, file=sys.stdout)
    annual_figure = go.Figure(
        data=[
            go.Bar(
                name="name",
                y=df[df.columns[i]],
                x=df[df.columns[0]],
                marker_color=OFFICIAL_COLOURS[i],
            )
            for i in range(1, len(df.columns))
        ]
    )
    annual_figure.update_layout(
        xaxis_title="Time",
        yaxis_title="Yearly Differences (%)",
        font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"),
    )
    return annual_figure


def update_table(return_tab, no_portfolios, input_money):
    data_table = {}
    for i in range(0, no_portfolios):
        i = return_tab[i]
        name = i[1]
        diffs = i[0][0]

        data_table.update(
            {
                f"{str(name[0])}  returns": diffs.astype(float).round(2),
                f"{str(name[0])} balance": (input_money + input_money * diffs)
                .astype(float)
                .round(2),
            }
        )

    df = pd.DataFrame(data_table).reset_index()
    df.rename(columns={"index": "date"})
    df["index"] = df["index"].dt.strftime("%Y")
    columns = [{"name": i, "id": i} for i in df.columns]

    data = df.to_dict("rows")

    annual_figure = dash_table.DataTable(data=data, columns=columns)

    return annual_figure


def print_dates(n_clicks, start_date, end_date):
    if n_clicks is None:
        raise PreventUpdate

    return f"Selected interval: {start_date} - {end_date}"
