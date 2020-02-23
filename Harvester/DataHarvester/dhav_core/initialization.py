"""
    Make sure that tickers exist
    Make sure that APIs have been initialized before
    This creates the persitent data csvs based on the tickers and apis used

"""
import pandas as pd
from os import listdir
from os.path import isfile, join


class Initializer:
    def __init__(self, api_list):
        self.api_list = api_list


    '''
        Based on the tickers available in the tickers folder
        this creates a update_list for each api
        each ticker will have Last Record,Earliest Record,
        and a Asset class.

        The update list is stored in persistant_data folder
        it is of the form: update_list_<api_name>.csv 
    '''

    def construct_update_list(self):
        pd.set_option("display.max_rows", None)
        ticker_files = [
            f for f in listdir("../tickers") if isfile(join("../tickers", f))
        ]
        # concatenate all tickers to construct the  update list
        frames = []

        for api in self.api_list:
            for ticker_f in ticker_files:
                ticker_f = ticker_f.replace("_tickers.csv", "")
                if ticker_f in api.supported_assets:
                    get_one_frame = pd.read_csv(
                        "../tickers/" + ticker_f + "_tickers.csv"
                    )
                    get_one_frame["Asset_Class"] = ticker_f
                    frames.append(get_one_frame)

            frames = pd.concat(frames, ignore_index=True)
            # frames = frames.drop(["Asset_Class"],axis=1)
            frames.to_csv("../persistant_data/update_list_" + api.name + ".csv")
            frames = []

        return 0

    '''
        The update position of each API is stored in a file
        called <api_name>_position.csv in the persistant_data
        folder.
        With each api call that gets data up until the current day
        the position is incremented by 1 by the DataHarvester
    '''

    def construct_position(self):
        names_dict = {}

        for x in range(len(self.api_list)):

            names_dict["Position Universal"] = 0
            frame_to_write = pd.DataFrame(names_dict, index=[0])
            frame_to_write.to_csv(
                "../persistant_data/" + self.api_list[x].name + "_position.csv"
            )
            names_dict = {}
        return 0
