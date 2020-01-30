from Thalia.dashboard import callbacks
import pytest
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go


def test_update_dashboard_prevents_update():
    with pytest.raises(PreventUpdate):
        callbacks.update_dashboard(*[None] * 7)
        pytest.fail("update_dashboard should not run on startup")


def test_update_dashboard():
    tickers = ("AAPL", "TSLA", None)
    proportions = (60, 40, None)
    fig, table_data = callbacks.update_dashboard(1, *tickers, *proportions)
    assert isinstance(fig, go.Figure), "update dashboard should return a plotly figure"
    # FIXME: below test is probably too tied to implementation
    assert all(row.get("metric") and row.get("value") for row in table_data)
