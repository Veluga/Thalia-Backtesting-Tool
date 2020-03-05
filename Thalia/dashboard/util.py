from functools import wraps
from Thalia.findb_conn import findb


def reader(f):
    wraps(f)
    reader = findb.conn.read

    def wrapper(*args, **kwargs):
        return f(reader, *args, **kwargs)

    return wrapper


@reader
def get_asset_names(reader):
    assets = reader.read_assets()
    names = assets['Name'].tolist()
    return names


@reader
def get_data(reader, tickers, start_date, end_date):
    # TODO: is calling list here too much coupling?
    asset_data = reader.read_asset_values(list(tickers), start_date, end_date)
    return asset_data


@reader
def get_dividends(reader, tickers):
    dividends = reader.read_assets_div_payout(tickers)
    return dividends
