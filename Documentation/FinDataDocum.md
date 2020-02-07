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
| FdMultiController.fd_create(db_name) | create and register a database named by string db_name return False if creation failed, True if sucesfull|
| FdMultiController.fd_connect(db_name, permissions_string) | Construct and return FdConnection object connected to database db_name. FdConnection will have access to methods based on weather the following characters are in the permissions_string: <br> - r : connection will have access to fd_read methods <br> - w : connection will have access to fd_write methods <br> - d : connection will have acces to df_remove methods <br> If df_name not registered, or connection to the database fails, this method will raise an exception|
|fd_delete(db_name)| delete database named `db_name` and remove it from registry|

### Example usage

```
from <FinData/fd_manager> import FdMultiController

# First create a new database, if you accidentaly use
# a name that already exists you'll get an eror

FdMultiController.fd_create('mydbname')

#connect and specify permissions

conn = FdMultiController.fd_connect('mydbname', 'rw')


# Since r and w were set as the permissions for this connection,
# collections of methods fd_read and fd_write will be available for use

conn.read.<fd_read_method>(...)
conn.write.<fd_write_method>(...)

# If 'd' (remove) permissions were also selected the fd_remove methods could also be accessed like so:
# conn.remove.<df_remove_method>(...)

```

## fd_read
File fd_read contains methods related to reading data from a FinData database. These methods should be accesed through the connection object created by FdMultiController like so : `conn.read.<method_name>(...)`

### Method spec:

|Method|Spec|
|-----|-----|
|read_asset_classes()| Returns dataframe of asset all records of asset classes stored in database. <br> Format: `pandas.DataFrame {columns=[], index=[AssetClassName(String)]}` |
|read_assets_in_class(asset_class_name)| return records of all assets in Assets table, with AssetClassName field matching asset_class_name <br> Format: <br> `pandas.DataFrame{Columns: [Name(String), AssetClassName(String=assset_class_name)] Index: [AssetTicker(String)]}` |
|read_assets() | Return dataframe of assets similar to in read_assets_in_class but returns all records irrespective of asset class |
|read_asset_values(asset_tickers, startDate=None, endDate=None) | Returns dataframe of recrods of all asset values of assets with ticker in List\<String> asset_tickers with AssetValue.ADate field in inclusive range between startDate\<datetime.date> and endDate\<datetime.date>. One or both ends of range can remain unbounded. Format: <br> `pandas.DataFrame {Columns: [AOpen<Decimal.decimal>, AClose<Decimal.decimal, AHigh<Decimal.decimal>, ALow<Decimal.decimal>] Index: [AssetTicker<String>, ADate <datetime.date>]}` |
|read_assets_div_payout(asset_tickers)|Takes list of string of asset tickers as a parameter, and returns all records from table DividentPayout with AssetTicker matching any element. Returns `pandas.DataFrame        {Columns: [Payout<decima.Decimal>] Index: [AssetTicker<String>, PDate<datetime.date>]}`|

## fd_write
File fd_write contains methods related to writing as well as overwriting data in a FinData database. These methods should be accesed through the connection object created by FdMultiController like so: <br> ` conn.write.<method_name>(...)`

### Method spec:
|Method|Spec|
|-----|-----|
| write_asset_classes(asset_classes) | Write asset classes specified in nonempty pandas.Dataframe asset_classes to financial database. If record already exists in DB, quietly update. Df of assset classes of format: <br> `{Columns: [], Index: [AssetClassName<String>]}`|
| write_assets(assets)  | Write assets specified in nonempty pandas.Dataframe assets to financial database. If record already exists in DB, quietly update. Df of assset classes of format: <br> `{Columns: [Name<String>, AssetClassName<String>] Index: [AssetTicker<String>]}`|
|write_asset_values(values)| Write asset values specified in nonempty pandas.DataFrame values to database. If any of the records already exist, quietly overwrite them. <br> - If added data would generate 'holes in the data' (the series of dates an assetTicker has data stored for would no longer be continuous), the write will fail. <br> - If any of the records reference an AssetTicker not in any record in Asset table, module will complain. <br> Input pandas.Dataframe of format: <br> `{Columns: [AOpen<Decimal.decimal>, AClose<Decimal.decimal>, AHigh<Decimal.decimal>, ALow<Decimal.decimal>] Index: [AssetTicker<String>, ADate <datetime.date>]}`|
|write_dividend_payouts(payouts)|takes as parameter nonempty pandas.DataFrame of format: <br> ` {Columns: [Payout<decima.Decimal> Index: [AssetTicker<String>, PDate<datetime.date>]}` <br> Records are written to the database, checking that foreign key constraint on Asset.AssetTicker is not violated|

## fd_remove
File fd_remove contains methods related to cascade deletion of records from a FinData database. These methods should be accesed through the connection object created by FdMultiController like so: <br> ` conn.remove.<method_name>(...)`. These are usefull for testing and administration. Neither the Harverster not Thalia Web should really be using these.

### Method spec:

|Method|Spec|
|------|------|
|deleteValues(ticker, date)|Delete record from AssetValue with Ticker matching `ticker` and date mathcing `date`. `date` can be either string or datetime.date|
|delete_div_payouts(ticker)|delete all records of divident payouts for asset with ticker mathcing `ticker`|
|deleteAssets(self, ticker)| delete assets with ticker mathcing `ticker`. Deletion cascades to all asset values in table AssetValues that match `ticker`|
|deleteAssetClasses(assetclassname)|delete all asset classes with name `assetclassname`. Cascades to all assets and asset values in asset class|



## Notes on design decisions and implementation
