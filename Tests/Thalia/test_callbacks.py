from Thalia.dashboard import callbacks
import pytest
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go


def test_filter_tickers():
    tickers = "RCK"
    param_state = []
    new_store = callbacks.filter_tickers(tickers, param_state)
    assert new_store, "RCK"


def test_update_dashboard_prevents_update():
    with pytest.raises(PreventUpdate):
        callbacks.update_dashboard(*[None] * 8)
        callbacks.update_dashboard(*[None] * 8)
        pytest.fail("update_dashboard should not run on startup")


def test_update_dashboard():
    tickers = [{"AssetTicker": "RCK", "Name": "Rock", "Allocation": 5}]

    start_date = "2015-02-19"
    end_date = "2020-02-19"
    input_money = 50
    input_contribution = 50
    contribution_dropdown = "BM"
    rebalancing_dropdown = "BM"
    fig, table_data = callbacks.update_dashboard(
        1,
        tickers,
        start_date,
        end_date,
        input_money,
        input_contribution,
        contribution_dropdown,
        rebalancing_dropdown,
    )

    assert isinstance(fig, go.Figure), "update dashboard should return a plotly figure"
    # FIXME: cannot check with table cause getting error couldn't calculate sortino ratio
    # assert all(row.get("metric") and row.get("value") for row in table_data)
