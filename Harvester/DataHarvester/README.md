# Data Harvester

### Description
Automatic financial data collector and updater. The first implementation is designed to work with Thalia financial backtesting application, more specifically with anda in house developed library. All content should be placed in a sqlite db at the end. For serious use, use something serious.

Philosophy: If some data is free than I want it all.
Purpose: Get a good grade so we can get a nice job.

Succes criteria: Do not get banned by your ISP.
Critical advice depending on the version run: Do not run from your own IP or your organization's.

Extra tools JFF: a VPN with a random server connect script 

###Data available
Check the tickers folder to see available data.
US bonds and index funds are pulled trough yahoo finance, they do not require a account.
nomics api is for standard and crypto currencies. A account is required.

###Updating Rules
After the initialization each API has 2 files in persistant_data folder.
One is [api_name]_position.csv and it contains the next ticker to update position.
The second one is update_list_[api_name].csv and it has a list with all the tickers that can be updated with that API.

The order of updates is done in a circular way. If the last position has been reached then go to the last one.

The index always points to the position that is going to be updated





In developement. Uses matplotlib for testing. 
