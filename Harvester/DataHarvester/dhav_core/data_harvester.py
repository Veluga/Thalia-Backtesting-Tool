"""
    
        Made by Intern George
            TeEsts included


"""

import pandas_datareader as pdread
import pandas as pd
import nomics
from datetime import datetime, timedelta


class DataHarvester:
    def __init__(self, api_list):
        self.api_list = api_list
        pass

    """
        It is important to verify that the tickers are 
        printed in the correct format. In order to inspect
        what data will be put in the database.

        One of the initial ideas was to have the harvester in a
        comand line format.
    """

    def show_all_tickers_hr(self):

        pd.set_option("display.max_rows", None)

        all_bonds = pd.read_csv("../tickers/bonds_tickers.csv")
        print(all_bonds)
        print("Data for bonds tickers: https://etfdb.com/etfs/bond/treasuries/")

        all_index_funds = pd.read_csv("../tickers/index_funds_tickers.csv")
        print(all_index_funds)
        print(
            "Data for index funds tickers: https://www.marketwatch.com/tools/mutual-fund/top25largest"
        )

        all_currency = pd.read_csv("../tickers/currency_tickers.csv")
        print(all_currency)
        print(
            "https://gist.github.com/Chintan7027/fc4708d8b5c8d1639a7c#file-currency-symbols-csv"
        )

        all_crypto = pd.read_csv("../tickers/crypto_tickers.csv")
        print(all_crypto)
        print("Those are the big ones at the time of making this: 31.1.2020")

        all_comodities = pd.read_csv("../tickers/comodities_future_tickers.csv")
        print(all_comodities)
        print("https://www.purefinancialacademy.com/futures-markets")

    """
        Inspect specific asset class. Also shows the data source.
        Not so usefull now but it was helped with starting off the project.
        Will be replaced with a tickers class instead of whatever is here now.
        Not important for the time beeing.
        It also need manual adding of tickers wich is quite bad.
    """

    def show_tickers_for(self, asset_class):
        pd.set_option("display.max_rows", None)
        if asset_class == "index_fund":
            all_index_funds = pd.read_csv("../tickers/index_funds_tickers.csv")
            print(all_index_funds)
            print(
                "Data for index funds tickers: https://www.marketwatch.com/tools/mutual-fund/top25largest"
            )
        elif asset_class == "bonds":
            all_bonds = pd.read_csv("../tickers/bonds_tickers.csv")
            print(all_bonds)
            print("Data for bonds tickers: https://etfdb.com/etfs/bond/treasuries/")

        elif asset_class == "currency":
            all_currency = pd.read_csv("../tickers/currency_tickers.csv")
            print(all_currency)
            print(
                "https://gist.github.com/Chintan7027/fc4708d8b5c8d1639a7c#file-currency-symbols-csv"
            )

        elif asset_class == "crypto":
            all_crypto = pd.read_csv("../tickers/crypto_tickers.csv")
            print(all_crypto)
            print("Those are the big ones at the time of making this: 31.1.2020")

        elif asset_class == "comodities_future":
            all_comodities = pd.read_csv("../tickers/comodities_future_tickers.csv")
            print(all_comodities)
            print("https://www.purefinancialacademy.com/futures-markets")
        else:
            print("asset_class_not_available")

    """
        Returns the tickers for a asset class.
        Again this can be usefull if you are doing operations on tickers and stuff.
    """

    def get_tickers(self, asset_class):
        if asset_class == "bonds":
            return pd.read_csv("../tickers/bonds_tickers.csv")
        elif asset_class == "index_funds":
            return pd.read_csv("../tickers/index_funds_tickers.csv")
        elif asset_class == "currency":
            return pd.read_csv("../tickers/currency_tickers.csv")
        elif asset_class == "crypto":
            return pd.read_csv("../tickers/crypto_tickers.csv")
        elif asset_class == "comodities_future":
            return pd.read_csv("../tickers/comodities_future_tickers.csv")
        else:
            print("asset_class_unavailable")

    '''
        Makes the api call based on the asset_class and ticker given.
        Also need a start and end date.

        date format: "YYYY-MM-DD"

        If the start date is older than the oldest available date
        then the oldest available date is returned. 
    '''

    def get_data(self, asset_class, ticker, start_date, end_date):
        if (
            asset_class == "index_funds"
            or asset_class == "bonds"
            or asset_class == "comodities_future"
        ):
            return self.yahoo_get(asset_class, ticker, start_date, end_date)
        elif asset_class == "crypto" or asset_class == "currency":
            return self.nomics_get(asset_class, ticker, start_date, end_date)

    '''
        Wrapper for the yfinance/yahoo api 
        Checks if the ticker is in the tickers in the tickers folder.
        Not usefull in the curent form but a good check to do.

        Returns the dataframe that has been received.
        returns 1 if api call failed. and has a error message
    '''

    def yahoo_get(self, asset_class, ticker, start_date, end_date):

        # check if ticker exists in dataframe
        if ticker in pd.read_csv("../tickers/" + asset_class + "_tickers.csv"):
            print("Ticker is not in available tickers for selected asset_class")
        try:
            dataframe_retrieved = pdread.DataReader(
                ticker, start=start_date, end=end_date, data_source="yahoo"
            )
        except pdread._utils.RemoteDataError as err:
            print("API call did not work", err)
            return 1  # return 1 if fail to get dataframe
        return dataframe_retrieved

    '''
        The harvester has a list of apis. 
        This function returns the ApiCaller object from the DataHarvester
        api list based on name.
    '''

    def get_api_from_list(self, api_name):
        for api in self.api_list:
            if api.name == api_name:
                return api

    '''
        Wrapper for nomics api.
        nomics fails in a different way compared to yfinance call through pandas
        Because of this if a call fails is dealt with in a different manner
    '''

    def nomics_get(self, asset_class, ticker, start_date, end_date):

        api_from_dh_list = self.get_api_from_list("nomics")

        nomics_api = nomics.Nomics(api_from_dh_list.key)

        if asset_class != "currency" and asset_class != "crypto":
            print("only currency and crypto can be retreived with yahoo finance.")
            exit()

        # currency can be fiat or crypto

        currency = nomics_api.ExchangeRates.get_history(
            currency=ticker,
            start=start_date + "T00:00:00Z",
            end=end_date + "T00:00:00Z",
        )
        currency_pd = pd.DataFrame([currency])

        return currency_pd

    '''
        Returns the current index of a api from the persitant data.
        The ticker under the index has not been updated yet.
    '''

    def current_index(self, api):
        position_frame = pd.read_csv("../persistant_data/" + api.name + "_position.csv")
        return position_frame["Position Universal"][0]

    '''
        Moves the update index by 1
        If it reaches the end of the list starts again from the first position
    '''

    def next_index(self, api):
        position_frame = pd.read_csv("../persistant_data/" + api.name + "_position.csv")
        update_list = pd.read_csv("../persistant_data/update_list_" + api.name + ".csv")
        number_rows = update_list.shape[0]
        index_position = position_frame["Position Universal"][0]
        index_position += 1

        if index_position + 1 > number_rows:
            index_position = 0

        position_frame["Position Universal"][0] = index_position
        position_frame.to_csv(
            "../persistant_data/" + api.name + "_position.csv", index=False
        )
        return 0

    '''
        Updates the ticker under the index.
        Ignores API calls that do not work because the ticker does not exist.
    '''
    def update_on_index(self, api):
        up_list = pd.read_csv("../persistant_data/update_list_" + api.name + ".csv")
        index = self.current_index(api)

        ticker_under_index = up_list.iloc[index]
        start_date = ""
        # set end_date to yesterday
        end_date = datetime.date(datetime.now()) + timedelta(days=-1)

        end_date = end_date.strftime("%Y-%m-%d")

        # if end_date and Last Update are the same day it means that
        # a full circle has been done and updating can stop for this api
        if end_date == ticker_under_index["Last_Update"]:
            return "full_circle"

        if pd.isna(ticker_under_index["Last_Update"]):
            start_date = "1970-1-1"
        else:
            start_date = ticker_under_index["Last_Update"]

        # if data retrieval fails just go to the next ticker

        print("Ticker: " + ticker_under_index["Ticker"] + " " + api.name)

        data_set_retrieved = self.get_data(
            ticker_under_index["Asset_Class"],
            ticker_under_index["Ticker"],
            start_date,
            end_date,
        )

        '''
            The code below updates the oldest record based on the data 
            received from the api.
        '''
        if type(data_set_retrieved) is not int and api.name == "yfinance":
            start_date = data_set_retrieved.first_valid_index()
            start_date = start_date.date()

        
        elif api.name == "nomics" and not data_set_retrieved.empty:
            # remove the things that are not required
            start_date = data_set_retrieved[0].values[0]["timestamp"].split("T")[0]
            print(start_date)

        if type(data_set_retrieved) is not int and not data_set_retrieved.empty:
            self.write_to_up_list(api, start_date, end_date)
            self.mock_write_to_db(data_set_retrieved)

        #
        #   Insert behaviour for when blocked by the API
        #   Never been blocked by the API what is the behaviour
        #   just try except

        #
        #   Deal with the erros caused by api not working later
        #   Never had any erros could not find error for except
        #

        return 0

    '''
        Writes back in the persitant data update list.
        This is done after updating a ticker.
        At this moment the data in update list should corespond with the
        data in the database.
    '''

    def write_to_up_list(self, api, start_date, end_date):
        up_list = pd.read_csv("../persistant_data/update_list_" + api.name + ".csv")
        index = self.current_index(api)
        up_list.loc[index, "Last_Update"] = end_date
        up_list.loc[index, "Earliest_Record"] = start_date
        up_list.to_csv(
            "../persistant_data/update_list_" + api.name + ".csv", index=False
        )


    '''
        Start the updating process.
        Each API does as many calls as there are in the calls_per_run
        variable in the api wrapper.
    '''
    def start_updating(self):
        # go trough APIs

        for api in self.api_list:
            for x in range(api.api_calls_per_run):
                answer = self.update_on_index(api)

                if answer == 0:
                    self.next_index(api)
                elif answer == "full_circle":
                    break

    """
        Write to db. 
    """

    def mock_write_to_db(self, dataset_to_sql):
        pass
