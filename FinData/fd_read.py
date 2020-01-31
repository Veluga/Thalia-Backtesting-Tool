"""
Module containing methods for reading from financial data database
"""

import df_config as dfc

import pandas as pd
import sqlite3

#TODO: Remove this
from datetime import date

class FdRead:
    @staticmethod
    def get_asset_values(asset_tickers, startDate=None, endDate=None):
        """
        Summary:
        Return pd.dataframe of asset values in inclusive range from startDate
        to endDate for any of the tickers in list assetTickers (if either date
        not provided range unbounded on approp side)

        Args:
        assetTickers: List[String] | Names of asset tickers
        startDate: datetime.Date | lower bound on date
        endDate: datetime.Date | upper bound on date

        Return:
        Pandas dataframe of format:
        {Columns: [AssetTicker<String>, ADate<datetime.date>,
                   AOpen<Decimal.decimal>, AClose<Decimal.decimal>,
                   AHigh<Decimal.decimal>, ALow<Decimal.decimal>]
         Index: []}
        containing AssetValues with date between start and end date and assetTicker
        in assetTickers
        """
        # Optionally move name to seperate config file later
        conn = sqlite3.connect(dfc.DATABASE_NAME)
        # generate parameter list for subsitution
        generated_params = str(tuple([ '@p' + str(i) for i in range(len(asset_tickers))])).replace('\'', '')
        # construct query
        query = "SELECT * \
                 FROM AssetValue \
                 WHERE AssetValue.AssetTicker IN " + generated_params + ' '
        if(startDate != None):
            query += 'AND (AssetValue.ADate >= @st_date) '
            asset_tickers.append(str(startDate))
        if(endDate != None):
            query += 'AND (AssetValue.ADate <= @end_date) '
            asset_tickers.append(str(endDate))
        # read data into df
        df0 = pd.read_sql(
            query + ";",
            conn,
            params=asset_tickers
        )
        conn.close()
        # adjust index if neccesary
        df0.set_index("AssetTicker", inplace=True)
        return df0

    @staticmethod
    def get_assets():
        """
        Summary:
        Return data frame of names, tickers and asset class names for
        all financial assets currently stored in the database.

        Args:
        None

        Return:
        Pandas dataframe of format
        {Columns: [Name<String>, AssetClassName<String>]
                   Index: [AssetTicker<String>]}
        each row containing details of an asset
        currently saved in db

        Notes:
        If nothing stored will return empty dataframe of same format
        """
        # Optionally move name to seperate config file later
        conn = sqlite3.connect(dfc.DATABASE_NAME)
        # read data in df
        df0 = pd.read_sql(
            "SELECT * \
         FROM Asset",
            conn,
        )
        conn.close()
        # adjust index if neccesary
        df0.set_index("AssetTicker", inplace=True)
        return df0

    @staticmethod
    def get_assets_in_class(asset_class):
        """
        Summary:
        Return all assets in a specified asset class

        Args:
        assetClass: string | Name of asset class

        Return:
        Pandas dataframe of format
        {Columns: [Name<String>, AssetClassName<@assetClass>]
                   Index: [AssetTicker<String>]}
        each row containing details of an asset
        currently saved in db with asset class equal to assetClass

        Notes:
        - If assetClass not in database, return empty dataframe in format

        - Will return AssetClass row in dataframe despite all values being equal
        (this is so dataframe can be used with fdWrite library methods as-is)

        - Implements seperate query to getAssetClasses due to performance
        considerations (Large number of assets should not be in working memory
        unless needed)
        """
        # Optionally move name to seperate config file later
        conn = sqlite3.connect(dfc.DATABASE_NAME)
        # read data in df
        df0 = pd.read_sql(
            "SELECT * \
         FROM Asset \
         WHERE Asset.AssetClassName = $className;",
            conn,
            params={"className": asset_class},  # use params dict to sanitize input
        )
        conn.close()
        # adjust index if neccesary
        df0.set_index("AssetTicker", inplace=True)
        return df0

    @staticmethod
    def get_asset_classes():
        """
        Summary:
        Return data frame of asset class data for all financial assets
        currently stored in the database.

        Args:
        None

        Return:
        Pandas dataframe of format
        {Columns: [] Index: [AssetClassName<String>]}
        each row containing details of an assetClass
        currently stored in db

        Notes:
        If nothing stored will return empty dataframe of same format
        """
        # Optionally move name to seperate config file later
        conn = sqlite3.connect(dfc.DATABASE_NAME)
        # read data in df
        df0 = pd.read_sql(
            "SELECT * \
         FROM AssetClass",
            conn,
        )
        conn.close()
        # adjust index if neccesary
        df0.set_index("AssetClassName", inplace=True)
        return df0


# unit testing code, if you're reading this outside of branch db-adaptor
# quietly remove it, as i've already moved it to tests
'''
print(FdRead.get_assets())
print("#" * 100)
print(FdRead.get_asset_classes())
print("#" * 100)
print(FdRead.get_assets_in_class("PETROLIUM DERIVATIVE"))
print("#" * 100)
print(FdRead.get_assets_in_class("NOTACLASS"))
print("#" * 100)
print(FdRead.get_asset_values(['GLU', 'BRY','RCK' , 'NOTANASSET'] , date(year=2020, month=1, day=1), date(year=2020, month=1, day=3)))
'''