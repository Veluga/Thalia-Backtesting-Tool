'''
Module containing methods for reading from finData.md database
'''
import pandas as pd
import sqlite3

class fdRead:
    @staticmethod
    def getAssetsInClass():
        pass


    @staticmethod
    def getAssets():
        '''
        Summary:
        Return data frame of names, tickers and asset class names for all financial assets
        currently stored in the database.

        Input:
        None

        Return:
        Pandas dataframe of format
        {Columns: [Name<String>, AssetClassName<String>] Index: [AssetTicker<String>]}
        each row containing details of an asset
        currently saved in db

        Notes:
        If nothing stored will return empty dataframe of same format
        '''
        #Optionally move name to seperate config file later
        conn = sqlite3.connect("finData.db")
        #read data in df
        df0 = pd.read_sql(
        'SELECT * \
         FROM Asset',
        conn
        )
        conn.close()
        #adjust index if neccesary
        df0.set_index('AssetTicker', inplace=True)
        return df0

    @staticmethod
    def getAssetClasses():
        '''
        Summary:
        Return data frame of asset class data for all financial assets
        currently stored in the database.

        Input:
        None

        Return:
        Pandas dataframe of format
        {Columns: [] Index: [AssetClassName<String>]}
        each row containing details of an assetClass
        currently stored in db

        Notes:
        If nothing stored will return empty dataframe of same format
        '''
        #Optionally move name to seperate config file later
        conn = sqlite3.connect("finData.db")
        #read data in df
        df0 = pd.read_sql(
        'SELECT * \
         FROM AssetClass',
        conn
        )
        conn.close()
        #adjust index if neccesary
        df0.set_index('AssetClassName', inplace=True)
        return df0


#Testing code, if youre reading this outside of branch db-adaptor kindly
#remove it

print(fdRead.getAssets())
print('#' * 100)
print(fdRead.getAssetClasses())