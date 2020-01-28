import pandas as pd
import decimal
from decimal import Decimal
from datetime import date, timedelta

# TODO: figure out how to set it to 2 decimal places, not signicant figures.
# possibly use quantize
# decimal.getcontext().prec = 2


class Strategy:
    def __init__(
        self,
        start_date: date,
        end_date: date,
        starting_balance: Decimal,
        assets: [dict],
        contribution_dates,  # implements __contains__ for date
        contribution_amount: Decimal,
        rebalancing_dates,  # implements __contains__ for date
        risk_free_rate: pd.DataFrame,
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.starting_balance = starting_balance
        self.assets = assets
        self.contribution_dates = contribution_dates
        self.contribution_amount = contribution_amount
        self.rebalancing_dates = rebalancing_dates
        self.risk_free_rate = risk_free_rate


# INTERNAL
def _allocate_investments(
    balance: Decimal, asset_weights: [float], asset_vals: [Decimal]
) -> [Decimal]:
    return [
        balance * Decimal(weight) / price
        for (weight, price) in zip(asset_weights, asset_vals)
    ]


# INTERNAL
def _measure_weights(asset_vals: [Decimal]) -> [float]:
    # asset_vals is the current amount of money invested in each asset.
    total = sum(asset_vals)
    # TODO: what if total == 0?
    return [float(val / total) for val in asset_vals]


# TODO: DRY.
def total_return(strat) -> pd.Series:
    # Returns the value of the portfolio at each day in the time frame.

    dates = pd.date_range(strat.start_date, strat.end_date)

    ret = pd.Series(Decimal("0"), index=dates)
    balance = strat.starting_balance
    investments = _allocate_investments(  # How many "units" of each asset to buy.
        balance,
        [asset["weight"] for asset in strat.assets],
        [asset["values"].at[strat.start_date, "Open"] for asset in strat.assets],
    )
    for date in dates:
        if date in strat.contribution_dates:
            current_weights = _measure_weights(
                [balance * Decimal(investment) for investment in investments]
            )
            balance += strat.contribution_amount
            investments = _allocate_investments(
                balance,
                current_weights,
                [asset["values"].at[date, "Open"] for asset in strat.assets],
            )
        if date == strat.start_date or date in strat.rebalancing_dates:
            # Calculate the number of units bought in each asset.
            investments = _allocate_investments(
                balance,
                [asset["weight"] for asset in strat.assets],
                [asset["values"].at[date, "Open"] for asset in strat.assets],
            )
        # TODO: sum()
        balance = Decimal("0.00")
        for asset, weight in zip(strat.assets, investments):
            balance += (weight * asset["values"].at[date, "Open"]).quantize(
                Decimal("0.01")
            )
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
