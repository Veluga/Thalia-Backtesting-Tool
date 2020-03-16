import dash_html_components as html
from .elements import graph_box


def summary_dashboard():
    return html.Div(
        [
            html.Div(id="boxes-container", className="container"),
            graph_box("Total Returns over Time", figure={}, id="main-graph", size=12),
        ],
        className="columns is-multiline",
    )
