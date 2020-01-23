from decimal import Decimal

decimal.getcontext().prec = 2


def total_return(strat) -> {date: Decimal}:
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
