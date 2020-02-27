"""
    This has to corelate with what Finda is reading from.
    This could be a single module used by both.
"""

# I need a way to check if the result of what I did is what I expect it to be


import sys
import os
import pandas as pd

# find a better way to reach Finda
sys.path.append("../../../")

from Finda import FdMultiController


class DataBaseConstructor:
    def __init__(self):
        # can put some for the fd_connect
        self.conn = FdMultiController.fd_connect("asset", "rw")

    def asset_classes_list(self):
        basepath = "../tickers/"
        array_list = []
        for entry in os.listdir(basepath):
            if os.path.isfile(os.path.join(basepath, entry)):
                entry = entry.replace("_tickers.csv", "")
                array_list.append(entry)

        return array_list

    def create_db_connection(self):
        self.conn = FdMultiController.fd_connect("asset", "rw")

    def dh_pass_asset_classes_fd(self):
        asset_list = []
        asset_list = self.asset_classes_list()

        """
            Create a pandas.DataFrame of the format:
            {Columns: [], Index: [AssetClassName<String>]}
            Insert all asset classes .
        """

        data_frame_asset_class = pd.DataFrame({"AssetClassName": asset_list})
        data_frame_asset_class = data_frame_asset_class.set_index("AssetClassName")

        self.conn.write.write_asset_classes(data_frame_asset_class)
        del data_frame_asset_class

    """
        Write a assets to the db for.
        Example:
            Asset Class: index_funds            //names of assetclasses can be changed later
            ticker     : SPY
            Name       : Long name of the ticker ?
                    : S&P 500 

            Fromat from the documentation: {Columns: [Name<String>, AssetClassName<String>] Index: [AssetTicker<String>]}

    All tickers have to be passed to finda.
    Since there is no update mechanism only a overwrite
    """

    def dh_pass_tickers_fd(self):

        asset_class_list = self.asset_classes_list()

        path_tickers = os.path.abspath(__file__)
        path_tickers = os.path.dirname(path_tickers)
        path_tickers = os.path.dirname(path_tickers)
        path_tickers = os.path.join(path_tickers, "tickers")

        ticr_list = []
        # check if complete dataframe exists
        all_frames = []
        for ast_cls in asset_class_list:

            completion = ast_cls + "_tickers.csv"
            path_tickers = os.path.join(path_tickers, completion)
            data_frame = pd.read_csv(path_tickers)
            all_frames.append(data_frame)
            # add the asset class to the data frame
            data_frame["AssetClassName"] = ast_cls

            # Find the extend names of the tickers
            # repeat ticker names for the moment

            data_frame["Name"] = data_frame["Ticker"]
            path_tickers = os.path.dirname(path_tickers)

        frames = pd.concat(all_frames, ignore_index=True)
        pd.set_option("display.max_columns", None)

        df_asset = pd.DataFrame(
            {
                "AssetTicker": frames["Ticker"],
                "Name": frames["Name"],
                "AssetClassName": frames["AssetClassName"],
            }
        )
        df_asset = df_asset.set_index("AssetTicker")

        self.conn.write.write_assets(df_asset)


if __name__ == "__main__":

    # FdMultiController.fd_create("asset")
    dbc = DataBaseConstructor()

    dbc.create_db_connection()
    dbc.dh_pass_asset_classes_fd()
    dbc.dh_pass_tickers_fd()

