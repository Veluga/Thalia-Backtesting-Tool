from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
from ..config import OFFICIAL_COLOURS
import pandas as pd
import dash_table


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


def portfolios_figure(return_tab, no_portfolios):
    """
    Function that outputs the annual returns graph
    for all portfolios
    """
    data_table = {}
    names = []
    for i in range(0, no_portfolios):
        i = return_tab[i]
        name = i[1]
        names.append(name)
        diffs = i[0]

        data_table.update({f"{str(name)}  returns": diffs.astype(float).round(2)})

    df = pd.DataFrame(data_table).reset_index()

    df["index"] = df["index"].dt.strftime("%Y")
    annual_figure = go.Figure(
        data=[
            go.Bar(
                name=names[i - 1],
                y=df[df.columns[i]],
                x=df[df.columns[0]],
                marker_color=OFFICIAL_COLOURS[i - 1],
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


def update_table(return_tab, no_portfolios):
    """
    function that outputs a table with
    data for all portfolios
    """
    data_table = {}
    for i in range(0, no_portfolios):
        i = return_tab[i]
        name = i[1]
        diffs = i[0]
        total_returns = i[2]

        data_table.update(
            {
                f"{str(name)}  returns %": diffs.astype(float).round(2),
                f"{str(name)} balance": (
                    total_returns[
                        (total_returns.index.day == 1)
                        & (total_returns.index.month == 1)
                    ]
                ),
            }
        )

    df = pd.DataFrame(data_table).reset_index()
    df["index"] = df["index"].dt.strftime("%Y")
    columns = [{"name": i, "id": i} for i in df.columns]

    data = df.to_dict("rows")

    annual_table = dash_table.DataTable(
        data=data,
        columns=columns,
        style_cell={"textAlign": "right", "border": "1px black"},
        style_as_list_view=True,
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
        ],
        style_table={"overflowX": "scroll", "width": "1200px", "height": "700px"},
        style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
    )

    return annual_table


def print_dates(n_clicks, start_date, end_date):
    if n_clicks is None:
        raise PreventUpdate

    return f"Selected interval: {start_date} - {end_date}"
