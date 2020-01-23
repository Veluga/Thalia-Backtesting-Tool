import pandas as pd
import decimal
from decimal import Decimal

decimal.getcontext().prec = 2


class Strategy:
    def __init__(
        self,
        start_date: datetime.date,
        end_date: datetime.date,
        starting_balance: decimal.Decimal,
        assets: List[dict],
        contribution_interval: datetime.timedelta,
        contribution_amount: decimal.Decimal,
        rebalancing_interval: datetime.timedelta,
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


def total_return(strat) -> pd.Series:
    # Returns the value of the portfolio at each day in the time frame.
    pass


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
