from analyse_data import analyse_data as anda

from . import user_csv, util


def get_strategy(
    tickers,
    proportions,
    handles,
    start_date,
    end_date,
    input_money,
    contribution_amount,
    contribution_dates,
    rebalancing_dates,
):
    """
    Initializes and returns strategy object
    """
    # TODO: add error handling for ticker not found
    weights = [p for p in proportions if p is not None]
    normalise(weights)

    # Separate user-supplied data from Thalia-known data.
    user_assets = []
    thalia_tickers = []
    thalia_weights = []
    for ticker, weight, handle in zip(tickers, weights, handles):
        if handle is None:
            thalia_tickers.append(ticker)
            thalia_weights.append(weight)
        else:
            user_assets.append((ticker, weight, handle))

    thalia_data = get_assets(thalia_tickers, thalia_weights, start_date, end_date)
    user_supplied_data = [
        anda.Asset(ticker, weight, user_csv.retrieve(handle))
        for ticker, weight, handle in user_assets
    ]
    all_asset_data = user_supplied_data + thalia_data

    real_start_date = max(asset.values.index[0] for asset in all_asset_data)
    real_end_date = min(asset.values.index[-1] for asset in all_asset_data)

    if real_end_date < real_start_date:
        # raise Error
        return None, None

    strategy = anda.Strategy(
        real_start_date,
        real_end_date,
        input_money,
        all_asset_data,
        contribution_dates,
        contribution_amount,
        rebalancing_dates,
    )
    return strategy


def get_table_data(strat, total_return):
    """
    Return a list of key metrics and their values
    """
    returns = total_return
    table = [
        {"metric": "Initial Balance", "value": returns[strat.dates[0]]},
        {"metric": "End Balance", "value": returns[strat.dates[-1]]},
    ]
    try:
        # We can't use append here because we want the table
        # unaltered if anything goes wrong.
        table = table + [
            {"metric": "Best Year", "value": anda.best_year(strat)},
            {"metric": "Worst Year", "value": anda.worst_year(strat)},
            {"metric": "Max Drawdown", "value": anda.max_drawdown(strat)},
        ]
        table = table + [
            {"metric": "Sortino Ratio", "value": anda.sortino_ratio(strat, None)},
            {"metric": "Sharpe Ratio", "value": anda.sharpe_ratio(strat, None)},
        ]
    except anda.InsufficientTimeframe:
        print("Not enough enough data for best/worst year")
    except Exception:
        print("Could not calculate Sharpe/Sortino ratios")

    return table


def normalise(arr):
    """
    Changes arr in place, keeping the relative weights the same,
    but scaling it such that it totals to 1.
    """
    total = sum(arr)
    for i in range(len(arr)):  # We're mutating so we have to index horribly.
        arr[i] /= total


def get_assets(tickers, proportions, start_date, end_date):
    """
    Gets data for each ticker and puts it in an anda.Asset.
    Returns a list of all assets.
    """
    assert len(tickers) == len(proportions)
    data = util.get_data(tickers, start_date, end_date)
    data = data.rename(
        columns={"AOpen": "Open", "AClose": "Close", "ALow": "Low", "AHigh": "High"}
    )
    assets = []
    for tick, prop in zip(tickers, proportions):
        asset_data = data[(data.AssetTicker == tick)]
        only_market_data = asset_data[["ADate", "Open", "Close", "Low", "High"]]
        only_market_data.index = only_market_data["ADate"]
        assets.append(anda.Asset(tick, prop, only_market_data))
    return assets
