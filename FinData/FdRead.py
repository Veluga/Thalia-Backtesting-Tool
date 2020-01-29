'''
Module containing methods for reading from finData.md database
'''
import pandas as pd
import sqlite3
import typing

class FdRead:
    @staticmethod
    def get

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
    def getAssetsInClass(assetClass):
        '''
        Summary:
        Return all assets in a specified asset class

        Input:
        assetClass: string | Name of asset class

        Return:
        Pandas dataframe of format
        {Columns: [Name<String>, AssetClassName<@assetClass>] Index: [AssetTicker<String>]}
        each row containing details of an asset
        currently saved in db with asset class equal to assetClass

        Notes:
        - If assetClass not in database, return empty dataframe in format

        - Will return AssetClass row in dataframe despite all values being equal
        (this is so dataframe can be used with fdWrite library methods as-is)

        - Implements seperate query to getAssetClasses due to performance
        considerations (Large number of assets should not be in working memory
        unless needed)
        '''
        #Optionally move name to seperate config file later
        conn = sqlite3.connect("finData.db")
        #read data in df
        df0 = pd.read_sql(
        'SELECT * \
         FROM Asset \
         WHERE Asset.AssetClassName = $className;',
        conn,
        params={'className':assetClass} #use params dict to sanitize input
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
#remove it, as ive already moved it to tests

print(FdRead.getAssets())
print('#' * 100)
print(FdRead.getAssetClasses())
print('#' * 100)
print(FdRead.getAssetsInClass('PETROLIUM DERIVATIVE'))
print('#' * 100)
print(FdRead.getAssetsInClass('NOTACLASS'))