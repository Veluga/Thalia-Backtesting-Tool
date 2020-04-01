import dash_html_components as html
import dash_core_components as dcc
from .elements import graph_box
import dash_table


def dates_container():
    return html.Div(
        html.Div(id="output-date", className="subtitle",),
        className="column is-12 has-text-right",
        style={"padding-bottom": "0px"},
    )


def returns_table(id):

    return html.Div(
        [
            html.P("Annual Returns", className="panel-heading"),
            dcc.Loading(
                html.Div(html.Div(id=f"return-table-{id}"),), className="panel-block",
            ),
        ],
        className="box",
    )


def returns_dashboard():
    return html.Div([returns_table(id=1), dates_container()])
