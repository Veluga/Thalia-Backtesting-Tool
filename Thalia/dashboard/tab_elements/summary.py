import dash_html_components as html
import dash_core_components as dcc
from .elements import graph_box


def dates():
    return html.Div(
        html.Div(id="output_dates", className="subtitle",), className="box",
    )


def annual_returns(id):
    return html.Div(
        [
            html.P("Annual Returns", className="panel-heading"),
            dcc.Loading(
                html.Div(
                    dcc.Graph(
                        id=f"annual-returns-{id}",
                        style={"width": "100%", "height": "400px"},
                    ),
                    className="panel-block",
                )
            ),
        ],
        className="box",
    )


def metrics_box(id, visibility, size):
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        html.Div(
                            id=f"box-Portfolio Name-{id}", className="level-item title"
                        ),
                        className="level",
                    ),
                    html.Hr(),
                    html.Div(
                        [
                            box_item("Initial Investment", id, unit="$"),
                            box_item("End Balance", id, unit="$"),
                        ],
                        className="level",
                    ),
                    html.Div(
                        [box_item("Best Year", id), box_item("Worst Year", id),],
                        className="level",
                    ),
                    html.Div(
                        [
                            box_item("Difference in Best Year", id, unit="%"),
                            box_item("Difference in Worst Year", id, unit="%"),
                        ],
                        className="level",
                    ),
                ],
                className="box",
                style={"background-color": "#efeae2 "},
            ),
            annual_returns(id),
        ],
        className=f"column is-{size} has-text-vcentered",
        style={"display": str(visibility)},
        id=f"metrics-box-{id}",
    )


def box_item(metric_name, id, unit=""):
    return html.Div(
        [
            html.Div(
                f"{metric_name}: ",
                className="title is-5",
                style={"padding-right": "1cm"},
            ),
            html.Div(id=f"box-{metric_name}-{id}", className="title is-5",),
            html.Div(unit),
        ],
        className="level-item",
    )


def portfolio_summary(id, reverse_layout=False):
    elements = [
        metrics_box(id, visibility="none", size=7),
        graph_box(
            "Asset Allocations",
            id=f"pie-{id}",
            size=5,
            visibility="none",
            height="650px",
        ),
    ]
    if reverse_layout:
        elements.reverse()

    return html.Div([html.Div(elements, className="columns")], className="column is-12")


def summary_dashboard():
    return html.Div(
        [
            graph_box(
                "Total Returns over Time",
                id="main-graph",
                size=12,
                visibility="block",
                height="600px",
            ),
            portfolio_summary(id=1),
            portfolio_summary(id=2, reverse_layout=True),
            portfolio_summary(id=3),
            portfolio_summary(id=4, reverse_layout=True),
            portfolio_summary(id=5),
        ],
        className="columns is-multiline",
    )
