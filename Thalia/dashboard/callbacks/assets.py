from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from ..config import MAX_PORTFOLIOS
from ..tab_elements.assets import asset_contributions_table_element


def register_assets_tab(dashapp):
    register_asset_contributions_table(dashapp)


def register_asset_contributions_table(dashapp):
    states = []
    for i in range(1, MAX_PORTFOLIOS + 1):
        states += [
            State(f"memory-table-{i}", "data"),
            State(f"portfolio-name-{i}", "value"),
        ]
    dashapp.callback(
        Output(f"assets-container", "children"),
        [Input("submit-btn", "n_clicks")],
        states,
    )(asset_contributions_table)


def asset_contributions_table(n_clicks, *args):
    if n_clicks is None:
        raise PreventUpdate

    table_data = args[0::2]
    portfolio_names = args[1::2]
    if None in table_data:
        no_portfolios = table_data.index(None)
    else:
        no_portfolios = MAX_PORTFOLIOS

    ret = [
        asset_contributions_table_element(portfolio_names[i], i, table_data[i])
        for i in range(no_portfolios)
    ]

    return ret
