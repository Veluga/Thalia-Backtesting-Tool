import dash_core_components as dcc
import dash_html_components as html

from . import tabs


layout = html.Div(
    html.Main(
        [
            html.Div(
                [
                    dcc.Store(id="memory-output"),
                    dcc.Tabs(
                        [
                            tabs.tickers(),
                            tabs.summary(),
                            tabs.metrics(),
                            tabs.returns(),
                            tabs.drawdowns(),
                            tabs.assets(),
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
