"""
Helper methods for finda testing
"""


import pandas as pd

from Finda import FdMultiController


def compare_df(dfT, dfR):
    """
    Compare dataframe values, columns and indecies regardless of column and index
    order
    """
    dfT = dfT.reindex(sorted(dfT.columns), axis=1)
    dfR = dfR.reindex(sorted(dfR.columns), axis=1)
    dfR = dfR.sort_index()
    dfT = dfT.sort_index()
    # assert (list(dfT.dtypes) == list(dfR.dtypes))
    assert pd.DataFrame.equals(dfR.sort_index(), dfT.sort_index())


def clear_DBs():
    # remove all financial database for testing environment
    for ndb in FdMultiController.fd_list():
        FdMultiController.fd_remove(ndb)
