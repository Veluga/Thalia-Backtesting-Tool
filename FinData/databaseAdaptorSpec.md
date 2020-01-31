
Global databases controller
---register and manage databases

Facade class, register connections, make it one object with permissions:

dbmanager('name' , 'rw')
use class composition to add submodules

yield

# Specification for the database adaptor module

Return pandas dataframe columns,
| Date | Index | Value |

Remember to add dependacies lewl

# Read

getAssets() : return PDDF of all assets

getAssetClasses() : return PDDF all asset classes

getCollectionOfAssets(list of tickers, startDate, endDate)
: return PDDF |ticker | date | values |

getAssInClass( class ) : return PDDF of assets rows related to a class, dont return
  -- return redundatnt rows (all class rows returned will be same), so its easier to operate (provide returned DF as input to) with write functions

# Write

insertAssets(PDDF)
  ticker, name, asset classes
check asset class there


insertValues(PDDF of format of assetValues table with DEcimal instead of text)
check assets are there
check that data is contiguous, and wouldnt create holes
quietly overwrites overlap

insertAssetClasses(PDDF of asset class names)

# Delete?
If given input not in db: doesnt complain ;;; this is by design andsomething SQLite does

deleteValues(PDDF)
    --Only need ticker + day columns

deleteAssets(PDDF)
    --Only need asset tickers
    will delete associated values

deleteAssetClasses(PDDF)
    -- only asset
    will delete associated assets and values


''Inserts with multiple values''

--- inputs are sanitized but types are not checked to keep in line with python
duck typing

--- if you try and query for exampla all assets in a class that isnt in the db
the software will return an empty dataframe. This is in line with how databases
and SQL in general act when queried. Upside is that programmer can process
requests without checking against available assets (and querying for them),
downside is that semantic errors with empty DF might be slightly harder to debug

--- three seperate modules : dfRead fdWrite fdRemove

for all write functions,
---  Use INSERT OR REPLACE
if given multiple rows to insert with same PK, no guaratnee as to witch one
ends up in the db

--- while its not the databases responsability to interpolate data, it should
ensure the data inside it is contiguous


--- always take df as input, even if only one value? why?

--- input output stored as text, passed as decimal

--- delete functions will delete associate data (deleting asset class deletes all assets, deletes all values) [because there should never be assets in a class that isnt in the asset class table]

--- can totaly compare ISO strings of dates

---  All transaction in SQLite are SERIALIZABLE, because SQLite controls concurrency via a database-wide read-write lock, so that there can only be one writer at a time