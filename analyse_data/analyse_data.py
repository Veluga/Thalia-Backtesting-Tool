import pandas as pd
import decimal
from decimal import Decimal
from datetime import date, timedelta
from collections import namedtuple

PENNY = Decimal("0.01")

Asset = namedtuple("Asset", ("ticker", "weight", "values"))
# ticker: str
# weight: Decimal
# values: pd.DataFrame("Open", "Low", "High", "Close") indexed and sorted by date.


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
        risk_free_rate: pd.DataFrame,
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
    balance = strat.starting_balance
    for date in strat.dates:
        if date == strat.dates[0] or date in strat.rebalancing_dates:
            investments = _allocate_investments(
                balance,
                [asset.weight for asset in strat.assets],
                [asset.values.at[date, "Close"] for asset in strat.assets],
            )
        if date in strat.contribution_dates:
            try:
                current_weights = _measure_weights(
                    [balance * holdings for holdings in investments]
                )
            except:
                current_weights = [asset.weight for asset in strat.assets]
            balance += strat.contribution_amount
            investments = _allocate_investments(
                balance,
                current_weights,
                [asset.values.at[date, "Close"] for asset in strat.assets],
            )
        balance = _calc_balance(investments, strat.assets, date)
        ret.at[date] = balance

    return ret


def sortino_ratio(strat) -> float:
    pass


def sharpe_ratio(strat) -> float:
    pass


def max_drawdown(strat) -> Decimal:
    pass


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
