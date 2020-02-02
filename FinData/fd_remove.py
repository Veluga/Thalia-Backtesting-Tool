import sqlite3
import pandas as pd


class fdremove:
    def __init__(self, db_address):
        self.db_address = db_address

    def create_connection(self, db_address):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_address)
        except sqlite3.error as e:
            print(e)

        return conn

    def select_all_values(self, conn):
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

    def select_all_assets(self, conn):
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

    def select_all_assets_classes(self, conn):
        """
        Query all rows in the assetsclass table
        :param conn: the Connection object
        :return:
        """
        df2 = pd.read_sql(
            'SELECT * \
            FROM AssetClass',
            conn
            )
        return df2

    def deleteValues(self, PDDF, ticker, date):

        '--Only need ticker + day columns'
        cur = conn.cursor()
        cur.execute('DELETE FROM AssetValue WHERE AssetTicker =? AND ADate=?',
                    (ticker, date))
        conn.commit()

    def deleteAssets(self, PDDF, ticker):
        '''
        --Only need asset tickers
        will delete associated values
        '''
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON")
        cur.execute('DELETE FROM Asset WHERE AssetTicker =? ', (ticker,))
        conn.commit()

    def deleteAssetClasses(self, PDDF, assetclassname):
        '''
        -- only asset
        will delete associated assets and values
        '''
        
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON")
        cur.execute('DELETE FROM AssetClass WHERE AssetClassName =? ', (assetclassname,))
        conn.commit()


fdr = fdremove('finData4.db')
conn = fdr.create_connection(fdr)
df0 = fdr.select_all_values(conn)
df1 = fdr.select_all_assets(conn)
df2 = fdr.select_all_assets_classes(conn)
#fdr.deleteValues(df0, 'ASS13', '2020-02-01')
#fdr.deleteAssets(df1, 'RCK')
fdr.deleteAssetClasses(df2, 'PETROLIUM DERIVATIVE')
print(df1)
print(df0)
print(df2)
