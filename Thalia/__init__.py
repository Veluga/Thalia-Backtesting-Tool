import dash
from config import Config
from flask import Flask
from flask.helpers import get_root_path
from flask_login import login_required


def create_app(test_config=None):
    server = Flask(__name__)
    server.config.from_object(Config)
    if test_config is not None:
        # load the test config if passed in
        server.config.update(test_config)

    register_dashapps(server)
    register_extensions(server)
    register_blueprints(server)

    return server


def register_dashapps(app):
    from .dashboard.layout import layout
    from .dashboard.callbacks import register_callbacks

    # Meta tags for viewport responsiveness
    meta_viewport = {
        # TODO: came with tutorial code, check if good enough
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no",
    }

    dashapp = dash.Dash(
        __name__,
        server=app,
        url_base_pathname="/dashboard/",
        assets_folder=get_root_path(__name__) + "/static/",
        meta_tags=[meta_viewport],
        suppress_callback_exceptions=True,
    )

    with app.app_context():
        dashapp.title = "Backtest dashboard"
        dashapp.layout = layout
        register_callbacks(dashapp)

    _protect_dashviews(dashapp)


def _protect_dashviews(dashapp):
    """
    prevent access to dash app without first login in
    """
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(
                dashapp.server.view_functions[view_func]
            )


def register_extensions(server):
    from .extensions import db
    from .extensions import login
    from .extensions import migrate

    db.init_app(server)
    login.init_app(server)
    login.login_view = "main.login"
    migrate.init_app(server, db)


def register_blueprints(server):
    from .views import server_bp

    server.register_blueprint(server_bp)
