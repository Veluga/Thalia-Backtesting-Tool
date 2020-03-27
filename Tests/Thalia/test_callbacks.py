from Thalia.dashboard import callbacks
import pytest
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import pandas as pd
from analyse_data import analyse_data as anda

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
    # create strategy
    start_date = pd.Timestamp(2000, 3, 12)
    end_date = pd.Timestamp(2000, 3, 16)
    asset_data = callbacks.get_assets(['OVF'], [1.0], start_date, end_date)
    strategy = anda.Strategy(
        start_date,
        end_date,
        1,
        asset_data,
        [],
        0,
        [],
    )
    assert callbacks.check_overfitting(strategy)
    '''
    asset_data = callbacks.get_assets(['NOVF'], [1.0], start_date, end_date)
    strategy = anda.Strategy(
        start_date,
        end_date,
        1,
        asset_data,
        [],
        0,
        [],
    )
    assert not callbacks.check_overfitting(strategy)
    '''