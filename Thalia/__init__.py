import dash
from config import Config
from flask import Flask
from flask.helpers import get_root_path
from flask_login import login_required


def create_app(test_config={}):
    server = Flask(__name__)
    server.config.from_object(Config)
    # load the test config if passed in otherwise nothing happens
    server.config.update(test_config)

    register_dashapps(server)
    register_extensions(server)
    register_blueprints(server)
    register_asset_db(server)

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

    external_stylesheets = [
        'https://cdn.jsdelivr.net/npm/bulma@0.8.0/css/bulma.min.css'
]

    dashapp = dash.Dash(
        __name__,
        server=app,
        url_base_pathname="/dashboard/",
        meta_tags=[meta_viewport],
        suppress_callback_exceptions=True,
        external_stylesheets=external_stylesheets
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


def register_asset_db(server, db_name="asset"):
    from Finda import fd_manager

    try:
        server.config.update(
            THALIA_DB_CONN=fd_manager.FdMultiController.fd_connect(db_name, "rwd")
        )
    except Exception as e:
        print("Fatal: Unable to connect to database " + db_name)
        print(e)
        exit()
