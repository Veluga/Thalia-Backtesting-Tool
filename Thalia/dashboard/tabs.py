import dash_core_components as dcc
import dash_html_components as html

tabs_styles = {"height": "44px"}
tab_style = {
    "borderBottom": "1px solid #d6d6d6",
    "padding": "6px",
    "fontWeight": "bold",
}

tab_selected_style = {
    "borderTop": "1px solid #d6d6d6",
    "borderBottom": "1px solid #d6d6d6",
    "backgroundColor": "#f26a4b",
    "color": "white",
    "padding": "6px",
}

tab_disabled_style = {
    "borderTop": "1px solid #d6d6d6",
    "borderBottom": "1px solid #d6d6d6",
    "backgroundColor": "#d6d6d6",
    "color": "white",
    "padding": "6px",
}


def title(title):
    return html.Div(
        html.H1(title, className="title"),
        className="column is-12",
        style={"padding-top": "2cm", "padding-bottom": "1cm"},
    )


def tickers():
    from .tab_elements.tickers import options_wrapper

    return dcc.Tab(
        label="Ticker Selection",
        children=[title("Select Constraints"), options_wrapper()],
        style=tab_style,
        selected_style=tab_selected_style,
        disabled_style=tab_disabled_style,
        id="tickers",
        value="tickers",
        disabled=False,
        className="has-text-vcentered",
    )


def summary():
    from .tab_elements.summary import summary_dashboard

    return dcc.Tab(
        label="Summary",
        children=[title("Portfolio Summary"), summary_dashboard()],
        style=tab_style,
        selected_style=tab_selected_style,
        disabled_style=tab_disabled_style,
        id="summary",
        value="summary",
        disabled=True,
    )


def metrics():
    from .tab_elements.metrics import table

    return dcc.Tab(
        label="Metrics",
        children=[title("Key Metrics"), table([], "table")],
        style=tab_style,
        selected_style=tab_selected_style,
        disabled_style=tab_disabled_style,
        id="metrics",
        value="metrics",
        disabled=True,
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
        style=tab_style,
        selected_style=tab_selected_style,
        disabled_style=tab_disabled_style,
        id="returns",
        value="returns",
        disabled=True,
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
        style=tab_style,
        selected_style=tab_selected_style,
        disabled_style=tab_disabled_style,
        id="drawdowns",
        value="drawdowns",
        disabled=True,
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
        style=tab_style,
        selected_style=tab_selected_style,
        disabled_style=tab_disabled_style,
        id="assets",
        value="assets",
        disabled=True,
    )