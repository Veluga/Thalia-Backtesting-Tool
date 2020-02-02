import sqlite3
import pandas as pd
import df_config as dfc


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.error as e:
        print(e)

    return conn


def select_all_values(conn):
    """
    Query all rows in the values table
    :param conn: the Connection object
    :return:
    pandas df (table values)
    """
    df0 = pd.read_sql(
        'SELECT * \
         FROM AssetValue',
        conn
        )
    return df0



def select_all_assets(conn):
    """
    Query all rows in the assets table
    :param conn: the Connection object
    :return:
    """
    df1 = pd.read_sql(
        'SELECT * \
         FROM Asset',
        conn
        )
    return df1


def deleteValues(PDDF, ticker, date):

    '--Only need ticker + day columns'
    cur = conn.cursor()
    cur.execute('DELETE FROM AssetValue WHERE AssetTicker =? AND ADate=?',
                (ticker, date))
    conn.commit()


def deleteAssets(PDDF, ticker):
    '''
    --Only need asset tickers
    will delete associated values
    '''
    cur = conn.cursor()
    cur.execute('DELETE FROM Asset WHERE AssetTicker =? ', (ticker,))
    #deleteValues(df0, (ticker, None))
    conn.commit()
'''
def deleteAssetClasses(PDDF):
    -- only asset
    will delete associated assets and values
'''


conn = create_connection(dfc.DATABASE_NAME)
df0 = select_all_values(conn)
df1 = select_all_assets(conn)
#deleteValues(df0, 'ASS13', '2020-02-01')
deleteAssets('RCK', 'ASS13')
print(df1)
print(df0)
