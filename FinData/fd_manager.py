"""
Module containing controler for the financial data database
"""

import sqlite3
import os
import pickle
import pandas as pd


import fd_read as fdr
import fd_write as fdw
import fd_remove as fdr


class FdMultiController:
    '''Controller object for managing multiple FinData databases

    Note:
    As of now this it is probably better to not use this feature,
    use FDController instead
    '''
    _db_registry_name = "registered"

    @staticmethod
    def _path_generator(f_name):
        """Convert name to path pointing to FinData direcroy
        """
        return os.path.join(
            os.path.split(os.path.abspath(__file__))[0], f_name + "." + "db"
        )

    @staticmethod
    def _fetch_names():
        """Return list of name of databases registered with FinData
        """
        try:
            fp = FdMultiController._path_generator(FdMultiController._db_registry_name)
            with open(fp, "rb") as pfile:
                names = pickle.load(pfile)
            return list(names)
        except IOError:
            return []

    @staticmethod
    def _add_name(db_name):
        """Add db_name to list of names of db registered with FdController
        """
        names = FdMultiController._fetch_names() + [db_name]
        file = open(FdMultiController._path_generator(FdController._db_registry_name), "wb")
        pickle.dump(names, file)
        file.close()

    @staticmethod
    def fd_list():
        """list databases created with FinData
        """
        return list(FdMultiController._fetch_names())

    @staticmethod
    def fd_create(db_name):
        """Create fin database at db_address with finData shchema

        Params:
        db_address : address at witch to create database

        Return:
        None

        Notes:
        -If db already registered, complain
        """
        # check db exists
        if db_name in FdController._fetch_names() + ["registered"]:
            raise Exception("DB already exists")
        # create database and read schema
        db_address = FdMultiController._path_generator(db_name)
        conn = None
        try:
            with open(FdMultiController._path_generator("dbSchema.sql")[:-3]) as file:
                conn = sqlite3.connect(db_address)
                curr = conn.cursor()
                curr.executescript(file.read())
                conn.close()
                FdController._add_name(db_name)
                return True
        except IOError:
            return False

    @staticmethod
    def fd_connect(db_name, permissions_string):
        """ Return controller for fdb with appropriate permissions

        Params:
        db_name: string, name of database
        permissions_string: string containg permissions flags

        Return:
        databse controller object linked to db at db_adress with methods
        correcponding to permissions string:
            - 'r' - read methods
            - 'w' - write methods
            - 'd' - methods for deleting records

        Notes:
            -If no valid SQLite database found at adress, excepts
        """
        # check db
        db_address = FdMultiController._path_generator(db_name)
        if db_name not in FdMultiController._fetch_names():
            raise Exception("DB name not registered with FinData controller")
        try:
            conn = sqlite3.connect(db_address)
            conn.close()
        except sqlite3.OperationalError:
            raise Exception(
                "Invalid or corrupted datbase found at address" + db_address
            )

        class FdConnection:
            def __init__(self):
                self.read = None
                self.write = None
                self.delete = None

        conn = FdConnection()
        if "r" in permissions_string:
            conn.read = fdr.FdRead(db_address)
        if "w" in permissions_string:
            conn.write = fdw.FdWrite(db_address)
        if "d" in permissions_string:
            # TODO: implement
            conn.remove = fdr.FdRemove(db_address)
        return conn


"""
Old unit tests, remove if necessary
"""
'''
df = pd.DataFrame(
    [
        {"AssetClassName": "BEVERAGE"},
        {"AssetClassName": "FLOOD"},
        {"AssetClassName": "MEDIA"},
    ]
)
df = df.set_index("AssetClassName")


fdc = FdController.fd_connect("data3", "rwd")

print(fdc.write.write_asset_classes(df))
print(fdc.read.read_asset_classes())
'''
