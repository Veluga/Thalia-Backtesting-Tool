import dash_html_components as html
from .elements import box, graph_box

def overfitting_button():
    return html.Div(
        html.Button(
            "Check Overfitting",
            "overfit-btn",
            className="button is-large is-primary",
            style={"background-color": "#f26a4b"},
        ),
        className="container has-text-centered",
    )

def overfitting_dashboard():
    return html.Div(
        [
            overfitting_button(),
            html.Br(),
            html.A("Check for possible overfitting in simulation."),
        ],
        className="columns is-multiline",
    )
