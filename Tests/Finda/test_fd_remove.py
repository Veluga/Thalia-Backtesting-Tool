import sqlite3

from Finda import fd_remove

con = sqlite3.connect("finData.db")
cur = con.cursor()
fdr = fd_remove.FdRemove('finData.db')


def test_delete_values():
    '''
    Test if deleteValaues method works based on the number of rows in the table
    using the seedDB.sh to populate the database
    Note: because of the cascade deleting, Asset Values has more rows deleted when running the other tests
    '''
    fdr.deleteValues('RCK', '2020-01-01')
    cur.execute('SELECT * FROM AssetValue')
    rs = cur.fetchall()
    #print(len(rs))
    assert len(rs) == 2


def test_delete_assets():
    '''
    Test if deleteAsset method works based on the number of rows in the table
    using the seedDB.sh to populate the database
    '''
    fdr.deleteAssets('BRY')
    cur.execute('SELECT * FROM Asset')
    rd = cur.fetchall()
    assert len(rd) == 2


def test_delete_assetclass():
    '''
    Test if deleteAssetclass method works based on the number of rows in the table
    using the seedDB.sh to populate the database
    '''
    fdr.deleteAssetClasses('CRYPTO')
    cur.execute('SELECT * FROM AssetClass')
    rs = cur.fetchall()
    assert len(rs) == 2


def test_delete_div():
    '''
    Test if deletediv method works based on the number of rows in the table
    using the seedDB.sh to populate the database
    '''
    fdr.delete_div_payouts('BRY')
    cur.execute('SELECT * FROM AssetClass')
    rs = cur.fetchall()
    assert len(rs) == 2


# conn = fd_remove.fdremove.create_connection()
print(test_delete_assetclass())
print(test_delete_assets())
print(test_delete_values())
print(test_delete_div())
