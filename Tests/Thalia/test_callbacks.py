from Thalia.dashboard import callbacks
import pytest
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import base64
import pandas as pd
from decimal import Decimal
from datetime import timedelta, date
import time
import os


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
    csv_data = (
        "Date,Open,High,Low,Close\n"
        "12/12/1980,0.51,0.50,0.51,0.51\n"
        "15/12/1980,0.48,0.48,0.48,0.48\n"
        "16/12/1980,0.45,0.45,0.45,0.45\n"
    )
    encoded = base64.b64encode(csv_data.encode("utf-8"))
    empty = os.listdir(callbacks.USER_DATA_DIR)
    handle = callbacks.store_user_asset(encoded, timeout=timedelta(seconds=2))
    assert empty != os.listdir(callbacks.USER_DATA_DIR)
    retrieved = callbacks.retrieve_user_asset(handle)
    expected = pd.DataFrame(
        [
            [Decimal("0.51"), Decimal("0.50"), Decimal("0.51"), Decimal("0.51")],
            [Decimal("0.51"), Decimal("0.50"), Decimal("0.51"), Decimal("0.51")],
            [Decimal("0.51"), Decimal("0.50"), Decimal("0.51"), Decimal("0.51")],
            [Decimal("0.48"), Decimal("0.48"), Decimal("0.48"), Decimal("0.48")],
            [Decimal("0.45"), Decimal("0.45"), Decimal("0.45"), Decimal("0.45")],
        ],
        columns=["Open", "High", "Low", "Close"],
        index=pd.date_range(date(1980, 12, 12), date(1980, 12, 16), freq="D"),
    )
    assert expected.equals(retrieved)
    time.sleep(4)
    assert empty == os.listdir(callbacks.USER_DATA_DIR)


