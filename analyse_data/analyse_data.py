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
        contribution_interval: timedelta,
        contribution_amount: Decimal,
        rebalancing_interval: timedelta,
        risk_free_rate: pd.DataFrame,
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.starting_balance = starting_balance
        self.assets = assets
        self.contribution_interval = contribution_interval
        self.contribution_amount = contribution_amount
        self.rebalancing_interval = rebalancing_interval
        self.risk_free_rate = risk_free_rate


# TODO: Pythonic use of iterators.
def total_return(strat) -> pd.Series:
    # Returns the value of the portfolio at each day in the time frame.

    dates = pd.date_range(strat.start_date, strat.end_date)

    stocks = []  # how many "stocks" you buy in each asset.
    for asset in strat.assets:
        stocks.append(
            Decimal(asset["weight"])
            * strat.starting_balance
            / asset["values"].at[strat.start_date, "Open"]
        )

    value = pd.Series(Decimal("0"), index=dates)
    for date in dates:
        for asset, weight in zip(assets, stocks):
            value.at[date] += weight * asset["values"].at[date, "Open"]

    return value


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
    start = date(2000, 1, 1)
    end = date(2000, 1, 7)

    dates = pd.date_range(start=start, end=end, freq="D")

    starting_balance = Decimal("23.46")
    contribution_interval = None
    contribution_amount = None
    rebalancing_interval = None

    gold_prices = [
        [Decimal("1"), Decimal("0.0")],
        [Decimal("4"), Decimal("0.0")],
        [Decimal("9"), Decimal("0.0")],
        [Decimal("16"), Decimal("0.0")],
        [Decimal("25"), Decimal("0.0")],
        [Decimal("36"), Decimal("0.0")],
        [Decimal("49"), Decimal("0.0")],
    ]

    silver_prices = [
        [Decimal("0.5"), Decimal("0.6")],
        [Decimal("1.0"), Decimal("1.1")],
        [Decimal("1.5"), Decimal("1.6")],
        [Decimal("2.0"), Decimal("2.1")],
        [Decimal("2.5"), Decimal("2.6")],
        [Decimal("3.0"), Decimal("3.1")],
        [Decimal("3.5"), Decimal("3.6")],
    ]

    gold_data = pd.DataFrame(gold_prices, index=dates, columns=["Open", "Close"])
    silver_data = pd.DataFrame(silver_prices, index=dates, columns=["Open", "Close"])

    assets = [
        {"ticker": "GOLD", "weight": 0.3, "values": gold_data},
        {"ticker": "SLV", "weight": 0.7, "values": silver_data},
    ]

    risk_free_rate = None

    strategy = Strategy(
        start,
        end,
        starting_balance,
        assets,
        contribution_interval,
        contribution_amount,
        rebalancing_interval,
        risk_free_rate,
    )

    print(total_return(strategy))
