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


def box(
    portfolio_name,
    start_date,
    end_date,
    initial_amount,
    end_balance,
    max_drawdown,
    best_year,
    worst_year,
):
    return html.Div(
        [
            html.Div(
                [
                    html.Div(portfolio_name, className="title"),
                    html.Div(
                        [
                            box_item("Initial Investment", initial_amount),
                            box_item("End Balance", end_balance),
                        ],
                        className="level",
                    ),
                    html.Div(
                        [
                            box_item("Best Year", best_year),
                            box_item("Worst Year", worst_year),
                            box_item("Max Drawdown", max_drawdown),
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
