from functools import wraps
from Thalia.findb_conn import findb


def conn(f):
    wraps(f)
    conn = findb.conn

    def wrapper(*args, **kwargs):
        return f(conn, *args, **kwargs)

    return wrapper


@conn
def get_asset_names(conn):
    assets = conn.read.read_assets()
    names = assets["Name"].tolist()
    return names


@conn
def get_data(conn, tickers, start_date, end_date):
    # TODO: is calling list here too much coupling?
    asset_data = conn.read.read_asset_values(list(tickers), start_date, end_date)
    return asset_data


@conn
def get_dividends(conn, tickers):
    dividends = conn.read.read_assets_div_payout(tickers)
    return dividends
