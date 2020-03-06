from Thalia.findb_conn import findb


def get_asset_names():
    assets = findb.read.read_assets()
    names = assets["Name"].tolist()
    return names


def get_data(tickers, start_date, end_date):
    # TODO: is calling list here too much coupling?
    asset_data = findb.read.read_asset_values(tickers, start_date, end_date)
    asset_data = asset_data.reset_index()
    return asset_data


def get_dividends(tickers):
    dividends = findb.read.read_assets_div_payout(tickers)
    return dividends
