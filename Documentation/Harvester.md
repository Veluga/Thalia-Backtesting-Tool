#Data Harvester Documentation



##Technical
This is done in preparation for the final latex report.

###Requirements 
| Module | Description |
| ---         | ---                |
| pandas_datareader | Install from pip. It is a wrapper for many financial 	 APIs |
| pandas | Install from pip. Used for manipulating the data.|
| nomics | API for currencies and crypto. It requires to be installed locally since it is not on pip. The company making this might make it available on pip in the future.|
| Standard python3 modules| Already come with python3.  Just imports.|


##Design 

The purpose of the Harvester is to update the database. By updating the database we mean calling a API and asking for the data of a specific financial ticker. The API returns the requested data. The Harvester notes that the ticker has been updated in its own persistent storage and writes the data to the database.


####Initialization

Make the objects that hold data about the APIs. 

* A path to apis_access folder has to be given to API objects that require a key.
####ApiObject

|Method|  Details|Example|
|-------|-------------|--------|
|init()| api_name: string, supported_asset_classes: [strings srray], api_calls_per_run: int, path_to_keys_folder: string, has_key=Bool |ApiObject("nomics", ["crypto", "currency"], 10, path, True)|


####Initializer
The Harvester has some persistent data storage that helps with keeping track of the next ticker to update, the Latest Update Date and the Earliest Record for that specific ticker.

The Initializer creates a 2 files for each api that it gets. Those are a position file called \\<api_name\\> 



####DataHarvester Usage

|Method|Description|Example|
|------|-------|-----|
|init()|Needs a list of APIs that are used| DataHarvester([api1, api2])|
| .start_update()|Start the updating procees|DataHarvester.start_updating()  |


