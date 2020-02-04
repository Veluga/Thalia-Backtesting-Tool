import sys, pandas, sqlite3

import pytest
#import FinData
import fd_remove
#from . import fd_remove

con = sqlite3.connect("finData.db")
cur = con.cursor()
fdr = fd_remove.FdRemove('finData.db')


def delete_values_test():
    '''
    Test if deleteValaues method works based on the number of rows in the table
    using the seedDB.sh to populate the database
    Note: because of the cascade deleting, Asset Values has more rows deleted when running the other tests
    '''
    fdr.deleteValues('RCK', '2020-01-01')
    cur.execute('SELECT * FROM AssetValue')
    rs = cur.fetchall()
    print(len(rs))
    assert len(rs) == 2


def delete_assets_test():
    '''
    Test if deleteAsset method works based on the number of rows in the table
    using the seedDB.sh to populate the database
    '''
    fdr.deleteAssets('BRY')
    cur.execute('SELECT * FROM Asset')
    rd = cur.fetchall()
    print(len(rd))
    assert len(rd) == 2


def delete_assetclass_test():
    '''
    Test if deleteAssetclass method works based on the number of rows in the table
    using the seedDB.sh to populate the database
    '''
    fdr.deleteAssetClasses('CRYPTO')
    cur.execute('SELECT * FROM AssetClass')
    rs = cur.fetchall()
    print(len(rs))
    assert len(rs) == 2


def delete_div_test():
    '''
    Test if deletediv method works based on the number of rows in the table
    using the seedDB.sh to populate the database
    '''
    fdr.delete_div_payouts('BRY')
    cur.execute('SELECT * FROM AssetClass')
    rs = cur.fetchall()
    print(len(rs))
    assert len(rs) == 2


# conn = fd_remove.fdremove.create_connection()
print(delete_values_test())

print(delete_assets_test())

print(delete_assetclass_test())

print(delete_div_test())