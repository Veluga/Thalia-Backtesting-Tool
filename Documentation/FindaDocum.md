# Doccumentation for financial data database module interface



## fd_manager

### Overview
Contains the FdMultiController class, witch has several static methods responsible for:
- creating a new database for use by FinData module
- keeping track of registerd databases that can be accessed through the FinData module
- Creating FdConnection connection objects linked to a registered database, these can be used to access stored data
- Managing access permissions

### Method spec

The following methods are available through the FdMultiController class:

|Method|Spec|
|-----|-----|
| FdMultiController.fd_list() | retrn list of names of databases registered with FinData module |
| FdMultiController.fd_create(db_name) | create and register a database named `db_name`. return False if creation failed, True if sucesfull|
|FdMultiController.fd_remove(db_name)| remove database `db_name` from register and delete its data|
| FdMultiController.fd_connect(db_name, permissions_string) | construct and return `FdConnection` object connected to database `db_name`. FdConnection will have access to methods based on weather the following characters are in the string `permissions_string`: <br> - r : connection will have access to `fd_read` methods through `<FdConnection name>.read`<br> - w : connection will have access to `d_write` methods trhough `<FdConnection name>.write` <br> - d : connection will have acces to df_remove methods through `<FdConnection name>.remove` <br> If df_name not registered, or connection to the database fails, this method will raise an exception|
|fd_delete(db_name)| delete database named `db_name` and remove it from registry|

### Example usage

```

from Finda import FdMultiController

# First create a new database, if you accidentaly use
# a name that already exists you'll get an eror

# All db management should be done with methods of FdMultiController
FdMultiController.fd_create('mydbname')

#connect and specify permissions

conn = FdMultiController.fd_connect('mydbname', 'rw')


# all access to datbase should be done through connections generated FdMultiController
# Since r and w were set as the permissions for this connection,
# collections of methods fd_read and fd_write will be available for use
conn.read.<fd_read_method>(...)
conn.write.<fd_write_method>(...)

# If 'd' (remove) permissions were also selected the fd_remove  
# methods could also be accessed like so:
# conn.remove.<df_remove_method>(...)

```

## \<conn>.read methods(fd_read.py)
the read attribute of a `FdConnection` is instantiated to a `FdRead` object with access to methods related to reading data from a FinData database.

### Method spec:

|Method|Spec|
|-----|-----|
|read_asset_classes()| Returns dataframe of asset all records of asset classes stored in database. <br> Format: `pandas.DataFrame {columns=[], index=[AssetClassName(String)]}` |
|read_assets_in_class(asset_class_name)| return records of all assets in db with AssetClassName matching string `asset_class_name` <br> Format: <br> `pandas.DataFrame{Columns: [Name(String), AssetClassName(String=assset_class_name)] Index: [AssetTicker(String)]}` |
|read_assets() | Return dataframe of assets similar to in `read_assets_in_class` but returns all records irrespective of asset class |
|read_asset_values(asset_tickers, startDate=None, endDate=None) | Returns dataframe of recrods of all asset values of assets with ticker in LIST `[<String>] asset_tickers` with AssetValue. ADate field in inclusive range between `startDate\<datetime.date>` and `endDate\<datetime.date>`. One or both ends of range can remain unbounded. Format: <br> `pandas.DataFrame {Columns: [AOpen<Decimal.decimal>, AClose<Decimal.decimal, AHigh<Decimal.decimal>, ALow<Decimal.decimal>] Index: [AssetTicker<String>, ADate <datetime.date>]}` |
|read_assets_div_payout(asset_tickers)|Takes list `[\<string>] asset_tickers` of asset tickers as a parameter, and returns all recorded divident payouts with AssetTicker matching any element. <br> Returns `pandas.DataFrame        {Columns: [Payout<decimal.Decimal>] Index: [AssetTicker<String>, PDate<datetime.date>]}`|

## \<conn>.write methods(fd_write.py)
the write attribute of a `FdConnection` is instantiated to a `FdWrite` object with access to methods related to writing data to a FinData database. By deafault all methods quietly overwrite existing data, and enforce the following foreign key contraints:
- Asset.AssetClassName -> AssetClass.AssetClassName
- AssetValue.AssetTicker -> Asset.AssetTicker
- DividendPayout.AssetTicker -> Asset.AssetTicker

### Method spec:
|Method|Spec|
|-----|-----|
| write_asset_classes(asset_classes) | Write asset classes specified in nonempty `pandas.Dataframe` `asset_classes` to financial database. Df of assset classes of format: <br> `{Columns: [], Index: [AssetClassName<String>]}`|
| write_assets(assets)  | Write assets specified in nonempty `pandas.Dataframe` `assets` to financial database. Df of assset classes of format: <br> `{Columns: [Name<String>, AssetClassName<String>] Index: [AssetTicker<String>]}`|
|write_asset_values(values)| Write asset values specified in nonempty `pandas.DataFrame` `values` to database. <br> Input pandas.Dataframe of format: <br> `{Columns: [AOpen<Decimal.decimal>, AClose<Decimal.decimal>, AHigh<Decimal.decimal>, ALow<Decimal.decimal>] Index: [AssetTicker<String>, ADate <datetime.date>]}`|
|write_dividend_payouts(payouts)| takes as parameter nonempty `pandas.DataFrame` `payouts` of format: <br> ` {Columns: [Payout<decima.Decimal> Index: [AssetTicker<String>, PDate<datetime.date>]}`|

## \<conn>.remove methods(fd_remove.py)
the remove attribute of a `FdConnection` is instantiated to a `FdRemove` object with access to methods related to mass removal of datafrom a FinData database. Cascade deletion is enabled by default, making these methods more powerfull than the ones in `fd_write.py`.

### Method spec:

|Method|Spec|
|------|------|
|deleteValues(ticker, date)| Delete record from AssetValue with Ticker matching `ticker` and date mathcing `date`. `date` can be either string or datetime.date|
|delete_div_payouts(ticker)| Delete all records of divident payouts for asset with ticker mathcing `ticker`|
|deleteAssets(self, ticker)| Delete assets with ticker mathcing `ticker`. Deletion cascades to all asset values in table AssetValues that match `ticker`|
|deleteAssetClasses(assetclassname)|delete all asset classes with name `assetclassname`. Cascades to all assets and asset values in asset class |

