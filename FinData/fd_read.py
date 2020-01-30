"""
Module containing methods for reading from finData.md database
# TODO: Start using typing module
"""

import df_config as dfc
import pandas as pd
import sqlite3


class FdRead:
    @staticmethod
    def get_asset_values(asset_tickers, startDate=None, endDate=None):
        """
        Summary:
        Return pd.dataframe of asset values between startDate and endDate for
        any of the tickers in list assetTickers, if either date not provided
        do not bound on that side

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
        generated_params = str(
            tuple(["@p" + str(i) for i in range(len(asset_tickers))])
        ).replace("'", "")
        # read data into df
        df0 = pd.read_sql(
            "SELECT * \
             FROM AssetValue \
             WHERE AssetValue.AssetTicker IN "
            + generated_params
            + ";",
            conn,
            params=asset_tickers,
        )
        conn.close()
        # adjust index if neccesary
        df0.set_index("AssetTicker", inplace=True)
        return df0

    @staticmethod
    def get_structured_values(asset_tickers, startDate=None, endDate=None):
        """
        Summary:
        Return structured list of all values of assets in list assetTickers
        between startDate and endDate, if a date is None, do not limit

        Args:
        assetTickers: list[String] | Names of assetTickers
        startDate: datetime.Date | returns values after startDate
        endDate: datetime.Date | return values after endDate

        Return:
        List of [startDate:datetime.date, endDate:f, Assets]
        where Assets is List[Asset]
        and Asset is dict {'ticker':String, 'name':String, 'values':Values}
        and Values is pd.DataFrame of format
        {Columns: [open, close, high, low] all of type decimal.Decimal
        Index: [Date: datetime.date]}

        EG:
        [1.1.2020, 2.2.2020, [
            {'ASS1', 'Asset1', pd.DF([
                                        1.1.2020:[0,1,0.5,0.5],
                                        2.1.2020:[1,2,1.5,2],
                                        ...
                                     ])},
            {'ASS2', 'Asset2', pd.DF(...)},
            ...
        ]]

        Notes:
        - If asset not in DB, returns empty dataframe of Values

        - return format designed to fit neatly into Strategy interface
        used by BL library
        """
        pass

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
print(FdRead.get_assets())
print("#" * 100)
print(FdRead.get_asset_classes())
print("#" * 100)
print(FdRead.get_assets_in_class("PETROLIUM DERIVATIVE"))
print("#" * 100)
print(FdRead.get_assets_in_class("NOTACLASS"))
print(FdRead.get_asset_values(["GLU", "BRY", "RCK", "NOTANASSET"], 1, 2))
