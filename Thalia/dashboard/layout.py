import dash_core_components as dcc
import dash_html_components as html

from . import tabs


layout = html.Div(
    html.Main(
        [
            dcc.Location(id="page-location-url"),
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
                            tabs.overfitting(),
                        ],
                        id="tabs",
                        value="tickers",
                    ),
                ],
                className="column",
            ),
        ],
        className="columns",
    ),
    className="section",
)
