"""
Module containing controler for the financial data database
"""

import sqlite3
import os
import pickle

from . import fd_read as fdr
from . import fd_write as fdw
from . import fd_remove as fdd


class FdMultiController:
    """Controller object for managing multiple FinData databases

    Note:
    As of now this it is probably better to not use this feature,
    use FDController instead
    """

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
        except OSError:
            return []

    @staticmethod
    def _add_name(db_name):
        """Add db_name to list of names of db registered with FdController
        """
        names = FdMultiController._fetch_names() + [db_name]
        file = open(
            FdMultiController._path_generator(FdMultiController._db_registry_name), "wb"
        )
        pickle.dump(names, file)
        file.close()

    @staticmethod
    def fd_remove(db_name):
        """Unregister db and delete it
        """
        names = FdMultiController._fetch_names()
        names.remove(db_name)
        with open(
            FdMultiController._path_generator(FdMultiController._db_registry_name),
            "wb") as file:
            pickle.dump(names, file)
        os.remove(FdMultiController._path_generator(db_name))


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
        -Will overwrite existing files not registered with Finda
        """
        # check db exists
        if db_name in FdMultiController._fetch_names() + ["registered"]:
            raise Exception("DB " +  db_name + " already exists")
        try:
            os.remove(FdMultiController._path_generator(db_name))
        except Exception as e:
            pass
        # create database and read schema
        db_address = FdMultiController._path_generator(db_name)
        conn = None
        try:
            with open(FdMultiController._path_generator("dbSchema.sql")[:-3]) as file:
                conn = sqlite3.connect(db_address)
                curr = conn.cursor()
                curr.executescript(file.read())
                conn.close()
                FdMultiController._add_name(db_name)
                return True
        except Exception:
            #generic class used to account for OS and import exceptions
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

        conn = sqlite3.connect(db_address)
        conn.close()

        class FdConnection:
            def __init__(self):
                self.read = None
                self.write = None
                self.remove = None

        conn = FdConnection()
        if "r" in permissions_string:
            conn.read = fdr.FdRead(db_address)
        if "w" in permissions_string:
            conn.write = fdw.FdWrite(db_address)
        if "d" in permissions_string:
            # TODO: implement
            conn.remove = fdd.FdRemove(db_address)
        return conn
