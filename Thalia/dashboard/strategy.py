from analyse_data import analyse_data as anda
from . import util


def get_strategy(
    tickers,
    proportions,
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

    assets_data = get_assets(tickers, weights, start_date, end_date)

    real_start_date = max(asset.values.index[0] for asset in assets_data)
    real_end_date = min(asset.values.index[-1] for asset in assets_data)

    if real_end_date < real_start_date:
        # raise Error
        return None, None

    strategy = anda.Strategy(
        real_start_date,
        real_end_date,
        input_money,
        assets_data,
        contribution_dates,
        contribution_amount,
        rebalancing_dates,
    )
    return strategy


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
