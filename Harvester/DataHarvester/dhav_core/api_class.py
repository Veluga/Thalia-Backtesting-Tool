import pandas_datareader as pdread
import pandas as pd
from datetime import datetime
import nomics
import numpy as np

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

    # once the data format is decided upon pass all df trough here
    # and remove the adjuster code from dh
    def df_format_standardizer(self):
        pass

    def yahoo_df_format(self,df,ticker ):
        df.reset_index(level=0, inplace=True)
        df["Date"] = pd.to_datetime(
                df["Date"]
            ).apply(lambda x: x.date())

        df = df.rename(columns={"Date":"ADate","Adj Close":"AClose","Low":"ALow","High":"AHigh","Open":"AOpen"})
        df["AssetTicker"] = ticker
        df["IsInterpolated"] = 0

        df = df.drop(columns=["Volume","Close"])
       
        return df

    def yahoo_finance(self, asset_class, ticker, start_date, end_date):
        try:
            dataframe_retrieved = pdread.DataReader(
                ticker, start=start_date, end=end_date, data_source="yahoo"
            )

        except pdread._utils.RemoteDataError as err:
            print("API call did not work", err)
            return 1  # return 1 if fail to get dataframe

        return self.yahoo_df_format(dataframe_retrieved,ticker)

    def nomics_format(self,df,ticker):
        df = pd.DataFrame.from_dict(df)
        df = df.rename(
            columns={
                "timestamp": "ADate",
                "rate": "AClose",
            }  # this is close in fact but crypto is wierd
        )

        df["ADate"] = [
            datetime.strptime(word.split("T")[0], "%Y-%m-%d").date()
            for word in df["ADate"]
        ]
        df["AHigh"] = np.nan
        df["ALow"] = np.nan
        df["AOpen"] = np.nan
        df["AssetTicker"] = ticker
        df["IsInterpolated"] = 0

        return df

    def nomics(self, asset_class, ticker, start_date, end_date):

        nomics_api = nomics.Nomics(self.key)

        if asset_class != "currency" and asset_class != "crypto":
            print("only currency and crypto can be retreived with yahoo finance.")
            exit()

        currency = nomics_api.ExchangeRates.get_history(
            currency=ticker,
            start=start_date + "T00:00:00Z",
            end=end_date + "T00:00:00Z",
        )

        # implement standard API wrapper and data format across data harvester
        if(len(currency) == 0):
            return 1

        return self.nomics_format(currency,ticker)

    def call_api(self, asset_class, ticker, start_date, end_date):
        if self.name == "yfinance":
            return self.yahoo_finance(asset_class, ticker, start_date, end_date)
        elif self.name == "nomics":
            return self.nomics(asset_class, ticker, start_date, end_date)
