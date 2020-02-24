"""
    Simple wrapper that holds informations about the API
    In order to see how the api call is performed,
    go to dhav_function and,in DataHarvester check <name>_get
    functions 
"""


class ApiObject:
    def __init__(
        self, name, supported_assets, api_calls_per_run, path="", has_key=False
    ):
        self.name = name
        self.has_key = has_key
        self.supported_assets = supported_assets
        if self.has_key == True:
            f = open(path + name, "r")
            self.key = f.read().rstrip()
        else:
            self.key = False

        self.api_calls_per_run = api_calls_per_run

    def yahoo_finance(self, asset_class, ticker, start_date, end_date):
        


    def call_api(self,asset_class, ticker, start_date, end_date):
        if(self.name == "yfinance"):
            return self.yahoo_finance(asset_class, ticker, start_date, end_date)
        else(self.name == "nomics"):
            return self.nomics(asset_class, ticker, start_date, end_date)