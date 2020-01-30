import numpy as np
import pandas as pd
import decimal
import math
from decimal import Decimal, InvalidOperation
from datetime import date, timedelta
from collections import namedtuple

PENNY = Decimal("0.01")

Asset = namedtuple("Asset", ("ticker", "weight", "values"))
# ticker: str
# weight: Decimal
# values: pd.DataFrame("Open", "Low", "High", "Close") indexed and sorted by date.

APPROX_TDAY_PER_YEAR = 252
APPROX_DAY_PER_YEAR = 365


class Strategy:
    def __init__(
        self,
        start_date: date,
        end_date: date,
        starting_balance: Decimal,
        assets: [Asset],
        contribution_dates,  # implements __contains__ for date
        contribution_amount: Decimal,
        rebalancing_dates,  # implements __contains__ for date
        risk_free_rate: pd.Series,
    ):
        self.dates = pd.date_range(start_date, end_date, freq="D")
        self.starting_balance = starting_balance
        self.assets = assets
        self.contribution_dates = contribution_dates
        self.contribution_amount = contribution_amount
        self.rebalancing_dates = rebalancing_dates
        self.risk_free_rate = risk_free_rate


# INTERNAL
def _allocate_investments(
    balance: Decimal, asset_weights: [Decimal], asset_vals: [Decimal]
) -> [Decimal]:
    return [
        balance * weight / price for (weight, price) in zip(asset_weights, asset_vals)
    ]


# INTERNAL
def _measure_weights(asset_vals: [Decimal]) -> [Decimal]:
    # asset_vals is the current amount of money invested in each asset.
    total = sum(asset_vals)
    # TODO: what if total == 0?
    return [val / total for val in asset_vals]


# INTERNAL
def _calc_balance(invesments: [Decimal], assets: [Asset], day: date) -> Decimal:
    return sum(
        holdings * asset.values.at[day, "Close"]
        for holdings, asset in zip(invesments, assets)
    ).quantize(PENNY)


# TODO: make numpy and pandas do the work.
def total_return(strat) -> pd.Series:
    # Returns the value of the portfolio at each day in the time frame.

    ret = pd.Series(Decimal("0"), index=strat.dates)
    ideal_weights = np.array([asset.weight for asset in strat.assets])
    asset_values = [asset.values["Close"] for asset in strat.assets]
    balance = strat.starting_balance

    for date in strat.dates:
        if date == strat.dates[0] or date in strat.rebalancing_dates:
            investments = _allocate_investments(
                balance, ideal_weights, [values.at[date] for values in asset_values],
            )
        if date in strat.contribution_dates:
            try:
                current_weights = _measure_weights(
                    [balance * holdings for holdings in investments]
                )
            except InvalidOperation:  # no money
                current_weights = ideal_weights
            balance += strat.contribution_amount
            investments = _allocate_investments(
                balance, current_weights, [values[date] for values in asset_values],
            )
        balance = _calc_balance(investments, strat.assets, date)
        ret.at[date] = balance

    return ret


def _risk_adjusted_returns(strat: Strategy) -> [Decimal]:
    returns = total_return(strat)
    strat.risk_free_rate = strat.risk_free_rate.map(
        lambda x: Decimal(pow(math.e, math.log(x) / APPROX_DAY_PER_YEAR))
    )
    return [
        (returns[i] / returns[i - 1]) - strat.risk_free_rate[i]
        for i in range(1, returns.size)
    ]


def sortino_ratio(strat: Strategy) -> float:
    risk_adjusted_returns = _risk_adjusted_returns(strat)
    below_target_std = np.std(list(filter(lambda x: x < 0, risk_adjusted_returns)))
    return (
        np.mean(risk_adjusted_returns)
        / below_target_std
        * Decimal(math.sqrt(APPROX_DAY_PER_YEAR))
    )


def sharpe_ratio(strat: Strategy) -> float:
    risk_adjusted_returns = _risk_adjusted_returns(strat)
    return (
        np.mean(risk_adjusted_returns)
        / np.std(risk_adjusted_returns)
        * Decimal(math.sqrt(APPROX_DAY_PER_YEAR))
    )


def max_drawdown(strat: Strategy) -> Decimal:
    returns = total_return(strat)
    max_seen, max_diff = 0, 1
    for i in range(returns.size):
        max_seen = max(max_seen, returns[i])
        max_diff = min(max_diff, returns[i] / max_seen)
    return (1 - max_diff) * 100


def best_year(strat) -> float:
    """
    Returns the increase (hopefully) in value of the strategy over its
    best calendar year - beginning and ending on Jan. 1.
    """
    pass


def worst_year(strat) -> float:
    # Same convention as best_year
    pass


# TODO: move tests into the proper testing area.
if __name__ == "__main__":
    pass
