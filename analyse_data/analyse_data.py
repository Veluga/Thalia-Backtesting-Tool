import numpy as np
import pandas as pd
import math
from decimal import Decimal, InvalidOperation
from datetime import date
from dataclasses import dataclass

PENNY = Decimal("0.01")


@dataclass
class Asset:
    ticker: str

    weight: Decimal

    # pd.DataFrame("Open", "Low", "High", "Close") indexed and sorted by date.
    values: pd.DataFrame

    # pd.DataFrame("Dividend") indexed by date
    dividends: pd.DataFrame = pd.DataFrame()


APPROX_TDAY_PER_YEAR = 252
APPROX_DAY_PER_YEAR = 365.25


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
    ):
        self.dates = pd.date_range(start_date, end_date, freq="D")
        self.starting_balance = starting_balance
        self.assets = assets
        self.contribution_dates = contribution_dates
        self.contribution_amount = contribution_amount
        self.rebalancing_dates = rebalancing_dates


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
    return [val / total for val in asset_vals]


# INTERNAL
def _calc_balance(invesments: [Decimal], asset_vals: [Decimal]) -> Decimal:
    return sum(
        holdings * value for holdings, value in zip(invesments, asset_vals)
    ).quantize(PENNY)


# INTERNAL
def _collect_dividend(dividend: Decimal, holdings: Decimal, price: Decimal) -> Decimal:
    return holdings + (holdings * dividend) / price


# TODO: make numpy and pandas do the work.
def total_return(strat) -> pd.Series:
    # Returns the value of the portfolio at each day in the time frame.

    ret = pd.Series(Decimal("0"), index=strat.dates)
    ideal_weights = np.array([asset.weight for asset in strat.assets])
    asset_values = [asset.values["Close"] for asset in strat.assets]
    balance = strat.starting_balance

    for day in strat.dates:
        asset_vals_today = [values.at[day] for values in asset_values]
        if day == strat.dates[0] or day in strat.rebalancing_dates:
            investments = _allocate_investments(
                balance, ideal_weights, asset_vals_today
            )
        for idx, asset in enumerate(strat.assets):
            if day in asset.dividends.index:
                investments[idx] = _collect_dividend(
                    asset.dividends["Dividends"][day],
                    investments[idx],
                    asset_vals_today[idx],
                )
        if day in strat.contribution_dates:
            try:
                current_weights = _measure_weights(
                    [balance * holdings for holdings in investments]
                )
            except InvalidOperation:  # no money
                current_weights = ideal_weights
            balance += strat.contribution_amount
            investments = _allocate_investments(
                balance, current_weights, asset_vals_today,
            )
        balance = _calc_balance(investments, asset_vals_today)
        ret.at[day] = balance

    return ret


def _risk_adjusted_returns(strat: Strategy, risk_free_rate: pd.DataFrame) -> [Decimal]:
    returns = total_return(strat)
    """ flake8 doesn't like unused variables
    risk_free_rate_daily = risk_free_rate.map(
        lambda x: Decimal(pow(math.e, math.log(x) / APPROX_DAY_PER_YEAR))
    )
    """
    # TODO Risk free rate of return is assumed to be 0 for now
    return [
        (returns[i] / returns[i - 1]) - Decimal(1.000) for i in range(1, returns.size)
    ]


def sortino_ratio(strat: Strategy, risk_free_rate: pd.DataFrame) -> float:
    risk_adjusted_returns = _risk_adjusted_returns(strat, risk_free_rate)
    below_target_std = np.std(list(map(lambda x: min(0, x), risk_adjusted_returns)))
    return (
        np.mean(risk_adjusted_returns)
        / below_target_std
        * Decimal(math.sqrt(APPROX_DAY_PER_YEAR))
    )


def sharpe_ratio(strat: Strategy, risk_free_rate: pd.DataFrame) -> float:
    risk_adjusted_returns = _risk_adjusted_returns(strat, risk_free_rate)
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


def _relative_yearly_diff(returns: pd.Series) -> [Decimal]:
    all_dates = returns.index
    year_begins = [d for d in all_dates if d.month == d.day == 1]
    return [
        returns.at[next_year] / returns.at[this_year] - Decimal("1.0")
        for (this_year, next_year) in zip(year_begins, year_begins[1:])
    ]


# TODO: efficiency.
def best_year(strat) -> float:
    """
    Returns the increase (hopefully) in value of the strategy over its
    best calendar year - beginning and ending on Jan. 1, as a percentage.
    """
    returns = total_return(strat)
    return max(_relative_yearly_diff(returns)) * Decimal(
        "100"
    )  # Adjust for percentage.


def worst_year(strat) -> float:
    # Same convention as best_year
    returns = total_return(strat)
    return min(_relative_yearly_diff(returns)) * Decimal(
        "100"
    )  # Adjust for percentage.
