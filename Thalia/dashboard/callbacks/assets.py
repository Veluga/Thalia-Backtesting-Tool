from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from ..config import MAX_PORTFOLIOS

"""
Don't review just here for later
"""


def register_assets_tab(dashapp):
    register_asset_contributions_table(dashapp)


def register_asset_contributions_table(dashapp):
    dashapp.callback(
        [
            Output(f"asset-contributions-{i}", "data")
            for i in range(1, MAX_PORTFOLIOS + 1)
        ],
        [Input("submit-btn", "n_clicks")],
        [State(f"memory-table-{i}", "data") for i in range(1, MAX_PORTFOLIOS + 1)],
    )(asset_contributions_table)


def asset_contributions_table(n_clicks, *args):
    # TODO
    if n_clicks is None:
        raise PreventUpdate

    if None in args:
        no_portfolios = args.index(None)
    else:
        no_portfolios = 5

    ret = []
    for i in range(no_portfolios):
        ret.append(args[i])

    for i in range(no_portfolios, MAX_PORTFOLIOS):
        ret.append(None)

    return ret
