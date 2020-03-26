from analyse_data import analyse_data as anda


def get_table_data(strat, total_return, portfolio_name):
    """
    Return a list of key metrics and their values
    """
    returns = total_return
    table = [
        {"metric": "Initial Balance", portfolio_name: returns[strat.dates[0]]},
        {"metric": "End Balance", portfolio_name: returns[strat.dates[-1]]},
    ]
    try:
        # We can't use append here because we want the table
        # unaltered if anything goes wrong.
        table = table + [
            {"metric": "Best Year", portfolio_name: round(anda.best_year(strat), 2)},
            {"metric": "Worst Year", portfolio_name: round(anda.worst_year(strat), 2)},
            {
                "metric": "Max Drawdown",
                portfolio_name: round(anda.max_drawdown(strat), 2),
            },
        ]
        table = table + [
            {
                "metric": "Sortino Ratio",
                portfolio_name: round(anda.sortino_ratio(strat, None), 2),
            },
            {
                "metric": "Sharpe Ratio",
                portfolio_name: round(anda.sharpe_ratio(strat, None), 2),
            },
        ]
    except anda.InsufficientTimeframe:
        print("Not enough enough data for best/worst year")
    except Exception:
        print("Could not calculate Sharpe/Sortino ratios")

    return table


def combine_cols(table1, table2):
    """
    Combines two lists of dictionaries with equal lengths
    """
    to_return = []
    for i in range(len(table1)):
        temp = {**table1[i], **table2[i]}
        to_return.append(temp)
    return to_return
