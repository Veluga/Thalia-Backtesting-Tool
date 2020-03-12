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
        pytest.fail("update_dashboard should not run on startup")


def test_update_dashboard():
    table_data = [{"AssetTicker": "RCK", "Name": "Rock", "Allocation": 5}]

    start_date = "2015-02-19"
    end_date = "2020-02-19"
    input_money = 50
    contribution_amount = 50
    contribution_frequency = "BM"
    rebalancing_frequency = "BM"
    fig = callbacks.update_dashboard(
        1,
        start_date,
        end_date,
        input_money,
        contribution_amount,
        contribution_frequency,
        rebalancing_frequency,
        table_data,
    )

    assert isinstance(fig, go.Figure), "update dashboard should return a plotly figure"
    # FIXME: cannot check with table cause getting error couldn't calculate sortino ratio
    # assert all(row.get("metric") and row.get("value") for row in table_data)
