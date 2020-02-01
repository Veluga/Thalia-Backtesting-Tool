"""
Module containing methods for writing to financial database

#TODO: account for column order
"""

import sqlite3


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
            Asset(AssetTicker), raise
        """
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
        values.index = values.index.map(lambda x: (str(x[0]), str(x[1])))

        self.__insert_df(values, "AssetValue")


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

print(df1)

FdWrite.add_asset_values(df1)

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
