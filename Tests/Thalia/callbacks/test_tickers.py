from Thalia.dashboard.callbacks import tickers
from dash.exceptions import PreventUpdate
import pytest
from Thalia.dashboard.config import MAX_PORTFOLIOS


def test_filter_tickers():
    ticks = "RCK – Rock"
    param_state = []
    user_supplied_csv = None
    new_store = tickers.filter_tickers(
        ticks, user_supplied_csv, None, param_state
    )
    assert "RCK" in new_store[0]["AssetTicker"]

    with pytest.raises(PreventUpdate):
        tickers.filter_tickers(None, None, None, param_state)
        pytest.fail("No Update on empty ticker selection")


def test_add_portfolio():
    with pytest.raises(PreventUpdate):
        tickers.add_portfolio(None)
        pytest.fail("No Update before button press")

    with pytest.raises(PreventUpdate):
        tickers.add_portfolio(MAX_PORTFOLIOS)
        pytest.fail("No Update if number of portfolios have reached maximum")

    returned = tickers.add_portfolio(
        1,
        {"display": "block"},
        {"display": "none"},
        {"display": "none"},
        {"display": "none"},
        {"display": "none"},
    )

    expected = [{"display": "block"}] * 2 + [{"display": "none"}] * (MAX_PORTFOLIOS - 2)
    expected.append(False)
    assert returned == expected

    returned = tickers.add_portfolio(
        MAX_PORTFOLIOS - 1,
        {"display": "block"},
        {"display": "block"},
        {"display": "block"},
        {"display": "block"},
        {"display": "none"},
    )

    expected = [{"display": "block"}] * MAX_PORTFOLIOS
    expected.append(True)
    assert returned == expected
