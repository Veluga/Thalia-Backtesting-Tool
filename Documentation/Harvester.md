# Data Harvester Documentation

## Technical
This is done in preparation for the final latex report.

### Requirements 
| Module | Description |
| ---         | ---                |
| pandas_datareader | Install from pip. It is a wrapper for many financial 	 APIs |
| pandas | Install from pip. Used for manipulating the data.|
| nomics | API for currencies and crypto. It requires to be installed locally since it is not on pip. The company making this might make it available on pip in the future.|
| Standard python3 modules| Already come with python3.  Just imports.|


## Design 

The purpose of the Harvester is to update the database. By updating the database we mean calling a API and asking for the data of a specific financial ticker. The API returns the requested data. The Harvester notes that the ticker has been updated in its own persistent storage and writes the data to the database.


#### Initialization

Make the objects that hold data about the APIs. 
Run the initializer.
* A path to apis_access folder has to be given to API objects that require a key.

#### ApiObject

|Method|  Details|Example|
|-------|-------------|--------|
|init()| api_name: string, supported_asset_classes: [strings srray], api_calls_per_run: int, path_to_keys_folder: string, has_key=Bool |ApiObject("nomics", ["crypto", "currency"], 10, path, True)|


#### Initializer

The Harvester has some persistent data storage that helps with keeping track of the next ticker to update, the Latest Update Date and the Earliest Record for that specific ticker.

The Initializer creates a 2 files for each api that it gets. Those are a position file called &lt;api_name>_position.csv and a update_list&lt;api_name>.csv. The update list contains all the tickers from the asset classes supported by the api.

|Method|Details|Example|
|-----|------|--------|
|init()|Needs a api list| Initializer([api1, api2])|
|construct_circular_list()|Creates the update lists. It is called circular becuase it acts like a circular list.| Initializer.construct_circular_list()|
|construct_position()|Creates the csv where the update position is stored|construct_position()|



#### DataHarvester Usage
After making the api objects and running the initializer. Just create a DataHarvester Object and run DataHarvester.start_updating() every day or multiple times per day so that your database has the data from the previous day. For each start_updating each api will do a api_calls_per_run number of calls.




#### DataHarvester methods

##### Methods used when updating

|Method|Description|Example|Details|
|------|-------|-----|------|
|init()|Needs a list of APIs that are used| DataHarvester([api1, api2])|
| start_update()|Start the updating procees|DataHarvester.start_updating()|
|write_to_up_list()|api: ApiObject, start_date:"YYYY-MM-DD", end_date: "YYYY-MM-DD"|Internal|Writes to the persistent update list|
|get_data()| asset_class:String,ticker:String, start_date:"YYYY-MM-DD", end_date:"YYYY-MM-DD"|Internal|Makes the right API call based on the asset class given and the ticker|
|yahoo_get()| asset_class:String,ticker:String, start_date:"YYYY-MM-DD", end_date:"YYYY-MM-DD"|Internal|Calls pandas_datareader yfinance for data|
|nomics__data()| asset_class:String,ticker:String, start_date:"YYYY-MM-DD", end_date:"YYYY-MM-DD"|Internal|Calls nomics for data.|
|get_api_from_list()|api_name:String|Internal|Returns the api object based on its name.|
|current_index()|api: ApiObject|Internal|Returns the current index of the api from the persistent data file|
|next_index()|api: ApiObject|Internal|Increases the  index of the api from the persistent data file by 1. If it reaches the last position it resets to back to 0|
|write_to_db()|dataset: pandas.DataFrame|Internal| Not implemented yet.





##### Printing methods
Those methods were useful in the inception phase. They can be used in order to verify the integrity of the tickers the asset classes. 
Those functions have not been used in the updating or the database connecting process. They will probably be removed at a later date.




### How does the update work

|Step No.|Class|Method called| Parent Method |Current Method| Details|
|-----------|-------|-----------------|--------------------|---------------------|----------|
|     0      |main| DataHarvester.start_updating()| None| None| A python script is telling DataHarvester to start a  Update run|
|1|DataHarvester|update_on_index(api)|None|start_updating()| Loop trough the API list. For each API update api_calls_per_run number of tickers from the persistent update list.|
|2|DataHarvester|get_data(*with parameters)|start_updating()|update_on_index() | Based on the data in the persistent update list. If there is no Last update then request all data from 1970.1.1 up to yesterday. Otherwise request data from Last Update up yesterday.
|2.0|DataHarvester|get_data(*with parameters)|start_updating()|update_on_index() | If the Last Update date is yesterday it means that a full circle has been completed for this API. The next API in the api list will be updated.
|2.1|DataHarvester|yahoo_get(*with parameters)|start_updating()|update_on_index()|Call yeahoo_get if the data requested has to be retrieved with pandas_datareader/yfinance API |
|2.2|DataHarvester|nomics_get(*with parameters)|start_updating()|update_on_index()|Call nomics_get if the data requested has to be retrieved with nomics |
|3|DataHarvester|None|start_updating()|update_on_index()|Check if data has been received. If yes then change the start_date(Earliest Record ) to the first date in the dataset received. |
|4|DataHarvester|write_to_up_list()|start_updating()|update_on_index()|Update the persistent list with the data received|
|5|DataHarvester|write_to_db()|start_updating()|update_on_index()|Update the persistent list with the data received. RETURN to start_updating()|
|6|DataHarvester|next_index()|None|start_updating()|If the update succeeded or failed go to the next ticker. And keep updating this api until the list is finished or the number of api_calls_per_run is reached. Then go to the next api.|


#### Helper Scripts
##### reseter.py
It resets the persistent data used when updating. Using it allows you to run the harvester multiple times in the same day.
##### run_updates.py
Starts running the updates. Creates the yfinance api and nomics api. Run the reseter first to create the persistent files. If the directory does not exist make it first. 

