import pandas_datareader as pdread
import pandas as pd
import nomics
import os
from datetime import datetime, timedelta
import sys
from .logger_class import Logger


# find a better way to reach Finda
sys.path.append("../../../")
from Finda import FdMultiController


class DataHarvester:
    def __init__(self, api_list):
        self.api_list = api_list
        
        #FdMultiController.fd_register("asset")
        #self.conn = FdMultiController.fd_connect("asset", "rw")

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

                self.log.log_api_call(asset_class, ticker, start_date, end_date)
                df = api.call_api(asset_class, ticker, start_date, end_date)
                self.log.log_simple("api returned " + str(type(df)))
                return df

    """
        Returns the current index of a api from the persitant data.
        The ticker under the index has not been updated yet.
    """

    def current_index(self, api):
        path = os.path.dirname(__file__)
        path = os.path.dirname(path)
        path = os.path.join(path, "persistant_data/" + api.name + "_position.csv")
        position_frame = pd.read_csv(path)
        return position_frame["Position Universal"][0]

    """
        Moves the update index by 1
        If it reaches the end of the list starts again from the first position
    """

    def next_index(self, api):
        path = os.path.dirname(__file__)
        path = os.path.dirname(path)
        path = os.path.join(path, "persistant_data/" + api.name + "_position.csv")
        position_frame = pd.read_csv(path)

        path = os.path.dirname(path)
        path = os.path.join(path, "update_list_" + api.name + ".csv")

        update_list = pd.read_csv(path)

        number_rows = update_list.shape[0]
        index_position = position_frame["Position Universal"][0]
        index_position += 1

        if index_position + 1 > number_rows:
            index_position = 0

        position_frame["Position Universal"][0] = index_position

        path = os.path.dirname(__file__)
        path = os.path.dirname(path)
        path = os.path.join(path, "persistant_data/" + api.name + "_position.csv")
        
        position_frame.to_csv(path, index=False)
        return 0

    """
        Updates the ticker under the index.
        Ignores API calls that do not work because the ticker does not exist.
    """

    def update_on_index(self, api):
        path = os.path.dirname(__file__)
        path = os.path.dirname(path)
        path = os.path.join(path, "persistant_data/update_list_" + api.name + ".csv")
        up_list = pd.read_csv(path)
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
            self.log.log_simple("Updated all tickers for today for with current API")
            return "full_circle"

        if pd.isna(ticker_under_index["Last_Update"]):
            start_date = "1970-1-1"
        else:
            start_date = ticker_under_index["Last_Update"]
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            start_date = start_date + timedelta(days=1)
            start_date = str(start_date)

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
            self.log.log_simple(
                "Received data frame with data between "
                + str(start_date)
                + " - "
                + str(end_date)
                + "\n Writing to the database."
            )

            start_date = data_set_retrieved["ADate"][0]

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
        path = os.path.dirname(__file__)
        path = os.path.dirname(path)

        path = os.path.join(path, "persistant_data/update_list_" + api.name + ".csv")

        up_list = pd.read_csv(path)
        index = self.current_index(api)
        up_list.loc[index, "Last_Update"] = end_date
        if pd.isna(up_list.loc[index, "Earliest_Record"]):
            up_list.loc[index, "Earliest_Record"] = start_date

        up_list.to_csv(path, index=False)

    """
        Start the updating process.
        Each API does as many calls as there are in the calls_per_run
        variable in the api wrapper.
    """

    def start_updating(self):
        # go trough APIs
        self.log.log_simple("\n\nStarted update at: " + str(datetime.now()))

        for api in self.api_list:

            self.log.log_simple(
                "Started updating " + api.name + " at " + str(datetime.now())
            )

            self.log.log_simple(
                "Updating for "
                + api.name
                + " doing "
                + str(api.api_calls_per_run)
                + " calls"
            )

            for x in range(api.api_calls_per_run):
                answer = self.update_on_index(api)
                if answer == 0:

                    self.next_index(api)
                elif answer == 1:
                    self.next_index(api)
                elif answer == "full_circle":
                    break
            self.log.log_simple(
                "Finished updating " + api.name + " at " + str(datetime.now())
            )
        self.log.log_simple("Finished all  updates at: " + str(datetime.now()))

    """
        Interpolation 
    """

    def add_interpolation_to_df(self, df):
        pd.set_option('precision', 6)
        interpolated_df = pd.DataFrame(columns=df.columns)
        interpolated_df = pd.DataFrame({i[0]: pd.Series(dtype=i[1])
                    for i in df.dtypes.iteritems()},
                    columns=df.dtypes.index)

        interpolated_df.reset_index()
        if(df.shape[0] == 1):
            return df
        else:
            for index_rows in range(df.shape[0]-1):
                
                today = df["ADate"][index_rows]
                
                
                tomorrow = df["ADate"][index_rows+1]
                
                delta = tomorrow - today
                
                rows_interpolated = []
                #why is it losing precision out of nowhere
                df_today = df.loc[index_rows]
                df_today_app = df_today.to_frame().transpose()

                interpolated_df = interpolated_df.append(
                    df_today_app, ignore_index=True, sort=False
                )

                
                if delta.days > 1:

                    for index_days in range(delta.days - 1):
                        
                        interpolated_row = df_today.copy()

                        interpolated_row["ADate"] = today + timedelta(days=index_days + 1)

                        interpolated_row["IsInterpolated"] = 1
                        
                        interpolated_row = interpolated_row.to_frame().transpose()

                        rows_interpolated.append(interpolated_row)

                    df_rows = pd.concat(rows_interpolated, ignore_index=True, sort=True)
                    
                    interpolated_df = interpolated_df.append(
                        df_rows, ignore_index=True, sort=False
                    )

            
            return interpolated_df

    """
        {Columns: [AOpen<Decimal.decimal>, AClose<Decimal.decimal>, 
            AHigh<Decimal.decimal>, ALow<Decimal.decimal>, IsInterpolated<Integer>] 
            Index: [AssetTicker<String>, ADate <datetime.date>]}
    """

    def write_to_db(self, dataset_to_sql, ticker_name):
        self.log.log_simple("Start interpolation" + "dataframe shape: " + str(dataset_to_sql.shape))

        df_to_send = self.add_interpolation_to_df(dataset_to_sql)

        self.log.log_simple(
            "Data Frame Interpolated" + "dataframe shape: " + str(df_to_send.shape)
        )
        df_to_send = df_to_send.set_index(["AssetTicker", "ADate"])

        self.log.log_simple("Writing interpolted dataframe to DB")

        self.conn.write.write_asset_values(df_to_send)
