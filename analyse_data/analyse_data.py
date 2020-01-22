from decimal import Decimal

decimal.getcontext().prec = 2


def total_return(strat) -> {date: Decimal}:
    pass


def sortino_ratio(strat) -> float:
    pass


def sharpe_ratio(strat) -> float:
    pass


def max_drawdown(strat) -> Decimal:
    pass


def best_year(strat) -> float:
    pass


def worst_year(strat) -> float:
    pass
