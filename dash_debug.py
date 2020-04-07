import dash
from Thalia.templates.dash.dash_base import base_html
from Thalia.dashboard.layout import layout
from Thalia.dashboard.callbacks import register_callbacks

# Meta tags for viewport responsiveness
meta_viewport = {
    # TODO: came with tutorial code, check if good enough
    "name": "viewport",
    "content": "width=device-width, initial-scale=1, shrink-to-fit=no",
}

external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/bulma@0.8.0/css/bulma.min.css",
    "https://use.fontawesome.com/releases/v5.3.1/js/all.js",
]
dashapp = dash.Dash(
    __name__,
    url_base_pathname="/dashboard/",
    meta_tags=[meta_viewport],
    suppress_callback_exceptions=True,
    external_stylesheets=external_stylesheets,
)

dashapp.title = "Backtest dashboard"
dashapp.index_string = base_html
dashapp.layout = layout
register_callbacks(dashapp)

dashapp.run_server(debug=True)