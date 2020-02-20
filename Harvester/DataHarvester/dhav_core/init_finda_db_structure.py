'''
    This has to corelate with what Finda is reading from.
    This could be a single module used by both.
'''

import sys
import os
import pandas as pd

# find a better way to reach Finda
sys.path.append("../../../")

from Finda import FdMultiController

class DataBaseConstructor:

    def __init__(self):
        self.conn = ''

    def asset_classes_list(self):
        basepath = "../tickers/"
        array_list = []
        for entry in os.listdir(basepath):
            if os.path.isfile(os.path.join(basepath, entry)):
                entry = entry.replace("_tickers.csv", "")
                array_list.append(entry)
    
        return array_list

   
        
            
    '''
        Make db
    '''

    def create_db_connection(self):
        self.conn = FdMultiController.fd_connect("asset", "rw")

    """
        Look into the tickers folder and based on the tickers there
        create the list of asset classes
    """

    def dh_pass_asset_classes_fd(self):
        asset_list = []
        asset_list = self.asset_classes_list()

        """
            Create a pandas.DataFrame of the format:
            {Columns: [], Index: [AssetClassName<String>]}
            Insert all asset classes .
        """

        data_frame_asset_class = pd.DataFrame({'AssetClassName':asset_list})
        data_frame_asset_class = data_frame_asset_class.set_index('AssetClassName')

        self.conn.write.write_asset_classes(data_frame_asset_class)
        del data_frame_asset_class
    
    '''
        Write a assets to the db for.
        Example:
            Asset Class: index_funds            //names of assetclasses can be changed later
            ticker     : SPY
            Name       : Long name of the ticker ?
                    : S&P 500 

            Fromat from the documentation: {Columns: [Name<String>, AssetClassName<String>] Index: [AssetTicker<String>]}

    All tickers have to be passed to finda.
    Since there is no update mechanism only a overwrite
    '''

    def dh_pass_tickers_fd(self):   

        asset_class_list = self.asset_classes_list()

        path_tickers =  os.path.abspath(__file__)
        path_tickers = os.path.dirname(path_tickers)
        path_tickers = os.path.dirname(path_tickers)
        path_tickers = os.path.join(path_tickers,'tickers')
        
        ticr_list = []
        # check if complete dataframe exists
        all_df_frames = []
        for ast_cls in asset_class_list:
            
            completion = ast_cls+"_tickers.csv"
            path_tickers = os.path.join(path_tickers,completion)
            
            if df_exists == False:
                
                complete_data_frame = pd.read_csv(path_tickers)
                print(complete_data_frame)
                df_exists = True
            else:
                partial_data_frame = pd.read_csv(path_tickers)
                
                complete_data_frame.append(partial_data_frame,ignore_index=True)
            #print(complete_data_frame)
            path_tickers = os.path.dirname(path_tickers)

        #print(complete_data_frame)


        df_asset = pd.DataFrame({'AssetTicker':['SPY'],'Name':["S&P 500"],'AssetClassName':['index_funds']})
        df_asset = df_asset.set_index('AssetTicker')


        #self.conn.write.write_assets(df_asset)

if __name__ == "__main__":
    dbc = DataBaseConstructor()
    dbc.create_db_connection()
    dbc.dh_pass_asset_classes_fd()
    dbc.dh_pass_tickers_fd()