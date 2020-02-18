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


|Function|Description|