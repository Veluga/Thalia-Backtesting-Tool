"""
Module containing methods for writing to financial database

#TODO: account for column order
"""

import sqlite3
import pandas as pd
from fd_read import FdRead
import datetime


class FdWrite:
    def __init__(self, db_address):
        self.db_address = db_address

    def __chceck_df_format(self, df, names):
        """check set of df indecies and column names are euqal to set of names
        except if incorrect

        Params:
        df: pandas.DataFrame
        names: list or set of df names

        Return:
        None

        Notes:
        None
        """
        # check df in correct format
        if set(list(df.index.names) + list(df.columns)) != set(names):
            raise Exception("Incorrect DF format (check row and index labels)")

    def __insert_df(self, recordsDF, tableName):
        """Insert zero or more records from pandas df into specified table

        Params:
        records: pandas.DataFrame of rows corresponding to records in table
        named tableName and indexed by the primary key's

        Return:
        none

        Notes:
        -If fuplicate PK in db, quietly update
        """
        conn = sqlite3.connect(self.db_address)
        # one of SQLites wierder idiosyncracies, pragmas must be executed
        # for each connection
        conn.execute("PRAGMA foreign_keys = ON;")
        recordsDF.reset_index(inplace=True)
        # construct table fields so order independant
        row_pos = "(" + ",".join(recordsDF.columns) + ")"
        # construct rest of query
        query = "INSERT OR REPLACE INTO " + tableName + row_pos + " \n VALUES \n"
        row_params = "(" + ",".join(recordsDF.shape[1] * ["?"]) + ")"
        query += (",".join(recordsDF.shape[0] * [row_params])) + ";"
        # create parameters list
        params = [y for x in recordsDF.values.tolist() for y in x]

        conn.cursor().execute(query, params)
        conn.commit()
        conn.close()

    def write_asset_classes(self, asset_classes):
        """Add zero or more records of asset classes to fin database

        Params:
        asset_classes: pandas.DataFrame of format:
        {Columns: [], Index: [AssetClassName<String>]}
        | pandas dataframe containing records of asset classes to be
          stored in database

        Return:
        None

        Notes:
        - If given non unique PK, quietly update record
        """
        self.__chceck_df_format(asset_classes, ["AssetClassName"])
        self.__insert_df(asset_classes, "AssetClass")

    def write_assets(self, assets):
        """Add zero or more records of assets to fin database

        Params:
        asset_classes: pandas.DataFrame of format:
        {Columns: [Name<String>, AssetClassName<String>],
         Index: [AssetTicker<String>]}
        | pandas dataframe containing records of assets to be
          stored in database

        Return:
        None

        Notes:
        - If given non unique PK, quietly update record
        - If one or more records contain reference to AssetClassName not in
          AssetClass(AssetClassName), raise exception
        """
        self.__chceck_df_format(assets, ["Name", "AssetClassName", "AssetTicker"])
        self.__insert_df(assets, "Asset")

    def write_asset_values(self, values):
        """Add zero or more records of values to fin database

        Params:
        assets: Pandas dataframe of format
        {Columns: [AOpen<Decimal.decimal>, AClose<Decimal.decimal>,
                AHigh<Decimal.decimal>, ALow<Decimal.decimal>]
         Index: [AssetTicker<String>, ADate <datetime.date>]}

        Return:
        None

        Notes:
        - If given non unique PK, quietly update record
        - If one or more records contain reference to AssetTicker not in
            Asset(AssetTicker), raise exception
        - If data added to database would create holes, raise exception
        """
        # fix up df
        df1 = values
        # check that data in values continuous
        for ass_df in df1.groupby("AssetTicker"):
            i_d = [str(a) for a in list(ass_df[1].index.get_level_values("ADate"))]
            for rdatet in pd.date_range(min(i_d), max(i_d)).tolist():
                if str(rdatet.date()) not in i_d:
                    raise Exception("Inserted values must be continuous")
            # get latest date so far, if emtpy any data will do
            fdrc = FdRead(self.db_address)
            df2 = fdrc.read_asset_values([ass_df[0]])
            df2 = df2.reset_index()
            db_dates = list(df2["ADate"])
            # extend range to so consecutive dates on boundary now overlap
            if not db_dates == []:
                n_upper = min(db_dates) + datetime.timedelta(-1)
                n_lower = max(db_dates) + datetime.timedelta(1)
                db_dates += [n_upper, n_lower]
                db_dates = [str(a.date()) for a in (db_dates)]
                if not (
                    (min(i_d) in db_dates)
                    or (max(i_d) in db_dates)
                    or (min(i_d) < min(db_dates) and max(i_d) > max(db_dates))
                ):
                    raise Exception("Inserted values not continuous with data in db")

        # check df in right format
        self.__chceck_df_format(
            values,
            [
                "AOpen",
                "AClose",
                "AHigh",
                "ALow",
                "ADate",
                "AssetTicker",
                "IsInterpolated",
            ],
        )
        # fix date and decimal types
        values["AOpen"] = values["AOpen"].map(str)
        values["AClose"] = values["AClose"].map(str)
        values["AHigh"] = values["AHigh"].map(str)
        values["ALow"] = values["ALow"].map(str)
        values = values.reset_index()
        values["ADate"] = values["ADate"].map(str)
        values = values.set_index(["AssetTicker", "ADate"])
        self.__insert_df(values, "AssetValue")

    def write_dividend_payouts(self, payouts):
        """Add zero or more records of divident payouts to fin database

        Params:
        asset_classes: pandas.DataFrame of format:
        {Columns: [Payout<decima.Decimal>]
                   Index: [AssetTicker<String>, PDate<datetime.date>]}
        | pandas dataframe containing records of payouts to be
          stored in database

        Return:
        None

        Notes:
        - If given non unique PK, quietly update record
        - If one or more records contain reference to AssetTicker not in
          Asset(AssetTicker), raise exception
        """
        self.__chceck_df_format(payouts, ["PDate", "Payout", "AssetTicker"])
        self.__insert_df(payouts, "DividendPayout")

"""
Hacky unit tests. If youre reading this please quietly remove them as I've
moved them to test folder + added automation
"""
"""
import fd_read as fdr


df = pd.DataFrame(
    [
        {"AssetClassName": "BEVERAGE"},
        {"AssetClassName": "FOOD"},
        {"AssetClassName": "MEDIA"},
    ]
)
df = df.set_index("AssetClassName")

FdWrite.add_asset_classes(df)


df0 = pd.DataFrame(
    [
        {"AssetClassName": "FOOD", "AssetTicker": "ASS13", "Name": "AssetOne"},
        {"AssetClassName": "FOOD", "AssetTicker": "ASS2", "Name": "AssetTwo"},
        {"AssetClassName": "BEVERAGE", "AssetTicker": "ASS3", "Name": "AssetThree"},
    ]
)

df0 = df0.set_index("AssetTicker")

FdWrite.add_assets(df0)


df1 = pd.DataFrame(
    [
        {
            "AssetTicker": "ASS13",
            "ADate": "2020-02-01",
            "ALow": "1.0",
            "AHigh": "1",
            "AOpen": "1",
            "AClose": "1",
            "IsInterpolated": 1,
        },
        {
            "AssetTicker": "ASS13",
            "ADate": "2020-02-02",
            "ALow": "2.0",
            "AHigh": "2",
            "AOpen": "2",
            "AClose": "2",
            "IsInterpolated": 1,
        },
        {
            "AssetTicker": "ASS13",
            "ADate": "2020-02-03",
            "ALow": "3.0",
            "AHigh": "3",
            "AOpen": "3",
            "AClose": "3",
            "IsInterpolated": 0,
        },
    ]
)

df1 = df1.set_index(["AssetTicker", "ADate"])

import fd_manager as fdm

fdm.fd_create('testDB1')
conn = fdm.FdMultiController.fd_connect('testDB1', 'rwd')
conn.write.add_asset_values(df1)

from datetime import date

print(fdr.FdRead.get_asset_classes())
print("#" * 100)
print(fdr.FdRead.get_assets())
print("#" * 100)
print(
    fdr.FdRead.get_asset_values(
        ["ASS13", "ASS14"],
        date(day=1, month=1, year=1),
        date(day=1, month=1, year=2050),
    )
)
"""
