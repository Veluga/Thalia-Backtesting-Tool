import logging 
import pandas as pd
'''
    Made in a separate class because
    I was thinking on having 2 types of logging.
    Detailed one and a less detailed one that is easier
    to follow.
'''


class Logger:
    
    def __init__(self):
        logging.basicConfig(filename='dh.log', level=logging.INFO)
    
    def log_simple(self,message):
        logging.info(message)
    
    def log_api_call(self, asset_class, ticker, start_date, end_date):
        logging.info("calling for:\nasset_class: "+asset_class+ " ticker: "+ ticker
                             + " start_date : "+start_date 
                             + " end_date: " + end_date)

    def extended_log(self,message,df):
        '''
            Will implement this after merging.
        '''
        pass