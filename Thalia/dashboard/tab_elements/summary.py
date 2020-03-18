import dash_html_components as html
from .elements import metrics_box, graph_box


def summary_dashboard():
    return html.Div(
        [
            metrics_box(1, visibility="none", size=4),
            metrics_box(2, visibility="none", size=4),
            metrics_box(3, visibility="none", size=4),
            metrics_box(4, visibility="none", size=6),
            metrics_box(5, visibility="none", size=6),
            graph_box("Total Returns over Time", figure={}, id="main-graph", size=12),
        ],
        className="columns is-multiline",
    )
