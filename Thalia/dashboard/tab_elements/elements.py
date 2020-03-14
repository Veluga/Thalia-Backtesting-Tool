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


def box(metric_names, metric_values):
    return html.Div(
        [
            html.Div(
                [
                    html.Div(metric_names[0], className="heading"),
                    html.Div(str(metric_values[0]), className="title"),
                    html.Div(
                        [
                            box_item(metric_names[1], metric_values[1]),
                            box_item(metric_names[2], metric_values[2]),
                            box_item(metric_names[3], metric_values[3]),
                        ],
                        className="level",
                    ),
                ],
                className="box",
                style={"background-color": "#efeae2 "},
            )
        ],
        className="column is-4",
    )


def box_item(metric_name, metric_value):
    return html.Div(
        [
            html.Div(metric_name, className="heading"),
            html.Div(str(metric_value), className="title is-5",),
        ],
        className="level-item",
    )
