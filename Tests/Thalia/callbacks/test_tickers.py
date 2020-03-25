from Thalia.dashboard.callbacks import tickers
import pytest


def test_filter_tickers():
    ticks = "RCK"
    param_state = []
    new_store = tickers.filter_tickers(ticks, param_state)
    assert new_store, "RCK"
