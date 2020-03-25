from Thalia.dashboard.callbacks import dashboard
from Thalia.dashboard.config import MAX_PORTFOLIOS, NO_TABS
import pytest
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go

import datetime


def test_tab_switch():
    with pytest.raises(PreventUpdate):
        dashboard.tab_switch(1, None)
        pytest.fail("Tab Switch should fail on incomplete Data")

    with pytest.raises(PreventUpdate):
        dashboard.tab_switch(None)
        pytest.fail("Tab Switch should fail on if button has not been pressed")

    assert dashboard.tab_switch(1, []) == ["summary"] + [False] * (NO_TABS - 1)


def test_retrieve_args():
    args = [
        "Portfolio Name",
        "Contribution Amount",
        "Contribution Frequency",
        "Rebalancing Frequency",
        "Table of Tickers",
    ] * MAX_PORTFOLIOS

    returned = dashboard.retrieve_args(args)

    assert "Portfolio Name" in returned["Portfolio Names"]
    assert "Contribution Amount" in returned["Contribution Amounts"]
    assert "Contribution Frequency" in returned["Contribution Frequencies"]
    assert "Rebalancing Frequency" in returned["Rebalancing Frequencies"]
    assert "Table of Tickers" in returned["Ticker Tables"]


def test_get_no_portfolios():
    args = [1, 2, 3, 4, 5]
    assert dashboard.get_no_portfolios(args) == MAX_PORTFOLIOS
    assert dashboard.get_no_portfolios([]) == 0
    assert dashboard.get_no_portfolios([1, None]) == 1


def test_validate_dates():
    frequency = dashboard.validate_dates(
        start_date=datetime.datetime.now(),
        end_date=datetime.datetime.now(),
        frequency="None",
    )
    assert not frequency
    # TODO test nonempty


def test_validate_amount():
    assert dashboard.validate_amount(None) == 0
    assert dashboard.validate_amount(100) == 100


def test_hidden_divs_data():
    no_portfolios = MAX_PORTFOLIOS
    assert not dashboard.hidden_divs_data(no_portfolios)

    no_portfolios = 4
    no_hidden_components = 11
    assert len(dashboard.hidden_divs_data(no_portfolios)) == no_hidden_components


def test_update_dashboard_prevents_update():
    with pytest.raises(PreventUpdate):
        dashboard.update_dashboard(*[None] * 8)
        pytest.fail("update_dashboard should not run on startup")
