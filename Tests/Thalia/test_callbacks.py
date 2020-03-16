from Thalia.dashboard import callbacks
import pytest
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import base64
from datetime import timedelta


def test_filter_tickers():
    tickers = "RCK"
    param_state = []
    new_store = callbacks.filter_tickers(tickers, param_state)
    assert new_store, "RCK"


def test_update_dashboard_prevents_update():
    with pytest.raises(PreventUpdate):
        callbacks.update_dashboard(*[None] * 8)
        pytest.fail("update_dashboard should not run on startup")


def test_user_data():
    csv_data = "Date,Open,High,Low,Close\n12/12/1980,0.513393,0.515625,0.513393,0.513393\n"
    encoded = base64.b64encode(csv_data.encode("utf-8"))
    handle = callbacks.store_user_asset(encoded, timeout=timedelta(minutes=1))
    retrieved = callbacks.retrieve_user_asset(handle)
    print(retrieved)
