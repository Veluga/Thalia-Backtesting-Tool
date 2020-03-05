import dash_core_components as dcc
import dash_html_components as html


def title(title):
    return html.Div(
        html.H1(title, className="title"),
        className="column is-12",
        style={"padding-top": "3cm"},
    )


def tickers():
    from .tab_elements.tickers import options_wrapper

    return dcc.Tab(
        label="Ticker Selection",
        children=[title("Ticker Selection"), options_wrapper(),],
    )


def summary():
    from .tab_elements.summary import summary_dashboard

    return dcc.Tab(
        label="Summary", children=[title("Portfolio Summary"), summary_dashboard(),]
    )


def metrics():
    from .tab_elements.metrics import table

    return dcc.Tab(
        label="Metrics", children=[title("Key Metrics"), table([], "table"),]
    )


def returns():
    return dcc.Tab(
        label="Returns",
        children=[
            title("Returns"),
            dcc.Graph(
                figure={
                    "data": [
                        {"x": [1, 2, 3], "y": [2, 4, 3], "type": "bar", "name": "SF"},
                        {
                            "x": [1, 2, 3],
                            "y": [5, 4, 3],
                            "type": "bar",
                            "name": "Montréal",
                        },
                    ]
                }
            ),
        ],
    )


def drawdowns():
    return dcc.Tab(
        label="Drawdowns",
        children=[
            title("Drawdowns"),
            dcc.Graph(
                figure={
                    "data": [
                        {"x": [1, 2, 3], "y": [2, 4, 3], "type": "bar", "name": "SF"},
                        {
                            "x": [1, 2, 3],
                            "y": [5, 4, 3],
                            "type": "bar",
                            "name": "Montréal",
                        },
                    ]
                }
            ),
        ],
    )


def assets():
    return dcc.Tab(
        label="Assets",
        children=[
            title("Assets Breakdown"),
            dcc.Graph(
                figure={
                    "data": [
                        {"x": [1, 2, 3], "y": [2, 4, 3], "type": "bar", "name": "SF"},
                        {
                            "x": [1, 2, 3],
                            "y": [5, 4, 3],
                            "type": "bar",
                            "name": "Montréal",
                        },
                    ]
                }
            ),
        ],
    )
