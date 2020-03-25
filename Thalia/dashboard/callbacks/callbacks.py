from .assets import register_assets_tab
from .summary import register_summary_tab
from .tickers import register_tickers_tab
from .dashboard import register_dashboard


def register_callbacks(dashapp):
    # register_assets_tab(dashapp)
    register_summary_tab(dashapp)
    register_tickers_tab(dashapp)
    register_dashboard(dashapp)
