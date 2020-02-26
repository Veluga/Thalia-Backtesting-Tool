
import pandas_datareader as pdread
import pandas as pd
import nomics
from datetime import datetime, timedelta
import sys
from logger import Logger


# find a better way to reach Finda
sys.path.append("../../../")
from Finda import FdMultiController


class DataHarvester:
    def __init__(self, api_list):
        self.api_list = api_list
        self.conn = FdMultiController.fd_connect("asset", "rw")
        self.log = Logger()
    """
        Makes the api call based on the asset_class and ticker given.
        Also need a start and end date.

        date format: "YYYY-MM-DD"

        If the start date is older than the oldest available date
        then the oldest available date is returned. 
    """


    def get_data(self, asset_class, ticker, start_date, end_date):
    
        for api in self.api_list:
            if asset_class in api.supported_assets:
               
               self.log.log_api_call(api.name,asset_class, ticker, start_date, end_date)
               df = api.call_api( asset_class, ticker, start_date, end_date)
               self.log.log_simple("api returned " + str(type(df)))
               return df
    

    """
        Returns the current index of a api from the persitant data.
        The ticker under the index has not been updated yet.
    """

    def current_index(self, api):
       
        position_frame = pd.read_csv("../persistant_data/" + api.name + "_position.csv")
        return position_frame["Position Universal"][0]

    """
        Moves the update index by 1
        If it reaches the end of the list starts again from the first position
    """

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

    """
        Updates the ticker under the index.
        Ignores API calls that do not work because the ticker does not exist.
    """

    def update_on_index(self, api):
        up_list = pd.read_csv("../persistant_data/update_list_" + api.name + ".csv")
        index = self.current_index(api)

        ticker_under_index = up_list.iloc[index]
        ticker_name = up_list.iloc[index]["Ticker"]
        

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

        data_set_retrieved = self.get_data(
            ticker_under_index["Asset_Class"],
            ticker_under_index["Ticker"],
            start_date,
            end_date,
        )

        """
            Change this after data format accross apis has been standardized.
        """
        
        if type(data_set_retrieved) != int:
            self.log.log_simple("Call for: "+ticker_name +"worked.\n Writing to update_list and db")
            start_date = data_set_retrieved["Date"][0]

            self.write_to_up_list(api, start_date, end_date)
            self.write_to_db(data_set_retrieved, ticker_name)
            return 0
        else:
            return 1
    """
        Writes back in the persitant data update list.
        This is done after updating a ticker.
        At this moment the data in update list should corespond with the
        data in the database.
    """

    def write_to_up_list(self, api, start_date, end_date):
        up_list = pd.read_csv("../persistant_data/update_list_" + api.name + ".csv")
        index = self.current_index(api)
        up_list.loc[index, "Last_Update"] = end_date
        up_list.loc[index, "Earliest_Record"] = start_date
        
        up_list.to_csv(
            "../persistant_data/update_list_" + api.name + ".csv", index=False
        )

    """
        Start the updating process.
        Each API does as many calls as there are in the calls_per_run
        variable in the api wrapper.
    """

    def start_updating(self):
        # go trough APIs

        for api in self.api_list:
            for x in range(api.api_calls_per_run):
                answer = self.update_on_index(api)
                if answer == 0:
                    self.next_index(api)
                elif answer == 1:
                    self.next_index(api)
                elif answer == "full_circle":
                    break

    """
        Interpolation 
    """

    def add_interpolation_to_df(self, df):

        df["Interpolated"] = 0
        interpolated_df = pd.DataFrame(
            columns=[
                "Date",
                "High",
                "Low",
                "Open",
                "Close",
                "Volume",
                "Adj Close",
                "Interpolated",
            ]
        )
        interpolated_df.reset_index()
        for index_rows in range(df.shape[0] - 1):
            today = df["Date"][index_rows]

            tomorrow = df["Date"][index_rows + 1]

            delta = tomorrow - today

            rows_interpolated = []

            df_today = df.iloc[index_rows]
            df_today_app = df_today.to_frame().transpose()

            interpolated_df = interpolated_df.append(df_today_app, ignore_index=True,sort=False)

            if delta.days > 1:
                
                for index_days in range(delta.days - 1):
                    interpolated_row = df_today.copy()
                    
                    interpolated_row["Date"] = today + timedelta(days=index_days + 1)
                    
                    interpolated_row["Interpolated"] = 1
                    interpolated_row = interpolated_row.to_frame().transpose()

                    rows_interpolated.append(interpolated_row)

                df_rows = pd.concat(rows_interpolated,ignore_index=True,sort=True)
                
                interpolated_df = interpolated_df.append(df_rows, ignore_index=True,sort=False)

        return interpolated_df

    """
        {Columns: [AOpen<Decimal.decimal>, AClose<Decimal.decimal>, 
            AHigh<Decimal.decimal>, ALow<Decimal.decimal>, IsInterpolated<Integer>] 
            Index: [AssetTicker<String>, ADate <datetime.date>]}
    """

    def write_to_db(self, dataset_to_sql, ticker_name):
        df_to_send = self.add_interpolation_to_df(dataset_to_sql)
        df_to_send["AssetTicker"] = ticker_name

        """
        last changes in order to conform with the finda documentation
        can be moved upper in the code but at this time getting things to work
        is higher priority
        """
        # and this is where the reality colides with our ideal model
        # in the naming scheme and the meanings

        final_df = pd.DataFrame(
            {
                "AOpen": df_to_send["Open"],
                "AClose": df_to_send["Adj Close"],
                "AHigh": df_to_send["High"],
                "ALow": df_to_send["Low"],
                "IsInterpolated": df_to_send["Interpolated"],
                "AssetTicker": df_to_send["AssetTicker"],
                "ADate": df_to_send["Date"],
            }
        )
        final_df = final_df.set_index(["AssetTicker", "ADate"])
        print(final_df[:5])
        #self.conn.write.write_asset_values(final_df)

    """
        It is important to verify that the tickers are 
        printed in the correct format. In order to inspect
        what data will be put in the database.

        One of the initial ideas was to have the harvester in a
        comand line format.
    """

    def show_all_tickers_hr(self):

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

