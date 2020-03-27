from Thalia.dashboard import callbacks
import pytest
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import pandas as pd
from analyse_data import analyse_data as anda
from config import Config


def test_filter_tickers():
    tickers = "RCK"
    param_state = []
    new_store = callbacks.filter_tickers(tickers, param_state)
    assert new_store, "RCK"


def test_update_dashboard_prevents_update():
    with pytest.raises(PreventUpdate):
        callbacks.update_dashboard(*[None] * 8)
        pytest.fail("update_dashboard should not run on startup")


def test_check_overfitting(mock_finda):
    # make sure overfitting threshold is something reasonable to somethign reasonable
    Config.OVERFITTING_THRESH = 0.7
    # create strategy
    start_date = pd.Timestamp(2000, 3, 13)
    end_date = pd.Timestamp(2000, 3, 15)
    # Will trigger for any positive threshold (T = -1.7)
    asset_data = callbacks.get_assets(["OVF"], [1.0], start_date, end_date)
    strategy = anda.Strategy(start_date, end_date, 1, asset_data, [], 0, [],)
    assert callbacks.check_overfitting(strategy)
    # Will not triger for any reasonable threashold
    asset_data = callbacks.get_assets(["NOVF"], [1.0], start_date, end_date)
    strategy = anda.Strategy(start_date, end_date, 1, asset_data, [], 0, [],)
    assert not callbacks.check_overfitting(strategy)
    # All values, should never triger since performance should be the same
    start_date = pd.Timestamp(2000, 3, 9)
    end_date = pd.Timestamp(2000, 3, 18)
    asset_data = callbacks.get_assets(["NOVF"], [1.0], start_date, end_date)
    strategy = anda.Strategy(start_date, end_date, 1, asset_data, [], 0, [],)
    assert not callbacks.check_overfitting(strategy)
