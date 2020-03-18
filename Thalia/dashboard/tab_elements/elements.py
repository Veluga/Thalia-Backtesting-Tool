import dash_html_components as html
import dash_core_components as dcc


def graph_box(graph_name, visibility, id, size=6):
    return html.Div(
        html.Div(
            [
                html.P(graph_name, className="panel-heading"),
                dcc.Loading(
                    html.Div(
                        dcc.Graph(id=id, style={"width": "100%", "height": "100%"},),
                        className="panel-block",
                    )
                ),
            ],
            className="box",
        ),
        className=f"column is-{size}",
        id=f"graph-box-{id}",
        style={"display": str(visibility)},
    )
