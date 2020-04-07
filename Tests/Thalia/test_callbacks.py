from Thalia.dashboard import callbacks
import pytest
from dash.exceptions import PreventUpdate


def test_filter_tickers():
    tickers = "RCK"
    param_state = []
    user_supplied_csv = None
    new_store = callbacks.filter_tickers(tickers, user_supplied_csv, param_state)
    assert new_store, "RCK"


def test_update_dashboard_prevents_update():
    with pytest.raises(PreventUpdate):
        callbacks.update_dashboard(*[None] * 8)
        pytest.fail("update_dashboard should not run on startup")
