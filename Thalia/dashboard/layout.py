import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html as inner_html
import os

from . import tabs


def read_html(html_file):
    base_html_path = os.path.join(
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "./templates/dash",
        ),
        html_file,
    )

    with open(base_html_path, "r") as fin:
        base_html = fin.read()

    return base_html


def navbar():
    return html.Div(
        [
            inner_html.DangerouslySetInnerHTML(read_html("dash_navbar.html")),
            html.Hr(style={"margin-top": 0}),
        ],
    )


layout = html.Div(
    [
        navbar(),
        html.Div(
            html.Main(
                [
                    html.Div(
                        [
                            dcc.Tabs(
                                [
                                    tabs.tickers(),
                                    tabs.summary(),
                                    tabs.metrics(),
                                    tabs.returns(),
                                    tabs.drawdowns(),
                                    tabs.assets(),
                                ]
                            )
                        ],
                        className="column is-offset-1 is-10",
                    ),
                ],
                className="columns",
            ),
            className="section",
        ),
    ]
)
