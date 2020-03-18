import dash_html_components as html
from .elements import graph_box


def dates():
    return html.Div(
        html.Div(id="output_dates", className="subtitle",), className="box",
    )


def metrics_box(id, visibility, size):
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        html.Div(id=f"box-Portfolio Name-{id}", className="title"),
                        className="level",
                    ),
                    html.Div(
                        [
                            box_item("Initial Investment", id),
                            box_item("End Balance", id),
                        ],
                        className="level",
                    ),
                    html.Div(
                        [box_item("Best Year", id), box_item("Worst Year", id),],
                        className="level",
                    ),
                ],
                className="box",
                style={"background-color": "#efeae2 "},
            )
        ],
        className=f"column is-{size}",
        style={"display": str(visibility)},
        id=f"metrics-box-{id}",
    )


def box_item(metric_name, id):
    return html.Div(
        [
            html.Div(metric_name, className="heading"),
            html.Div(id=f"box-{metric_name}-{id}", className="title is-5",),
        ],
        className="level-item",
    )


def portfolio_summary(id, reverse_layout=False):
    elements = [
        metrics_box(id, visibility="none", size=6),
        graph_box("Asset Allocations", id=f"pie-{id}", size=6, visibility="none"),
    ]
    if reverse_layout:
        elements.reverse()

    return html.Div([html.Div(elements, className="columns")], className="column is-12")


def summary_dashboard():
    return html.Div(
        [
            graph_box(
                "Total Returns over Time", id="main-graph", size=12, visibility="block"
            ),
            portfolio_summary(id=1),
            portfolio_summary(id=2, reverse_layout=True),
            portfolio_summary(id=3),
            portfolio_summary(id=4, reverse_layout=True),
            portfolio_summary(id=5),
        ],
        className="columns is-multiline",
    )
