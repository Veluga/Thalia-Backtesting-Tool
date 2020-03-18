import dash_html_components as html
import dash_core_components as dcc


def dates():
    return html.Div(
        html.Div(id="output_dates", className="subtitle",), className="box",
    )


def graph_box(graph_name, figure, id, size=6):
    return html.Div(
        html.Div(
            [
                html.P(graph_name, className="panel-heading"),
                dcc.Loading(
                    html.Div(
                        dcc.Graph(
                            figure=figure,
                            id=id,
                            style={"width": "100%", "height": "100%"},
                        ),
                        className="panel-block",
                    )
                ),
            ],
            className="box",
        ),
        className=f"column is-{size}",
    )


def metrics_box(id, visibility, size):
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        html.Div(id=f"box-Portfolio Name-{id}", className="title"),
                        className="level has-text-centered",
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
