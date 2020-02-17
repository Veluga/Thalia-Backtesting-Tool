import pandas_datareader as pdread
import pandas as pd

from api_class import ApiCaller as apic
from dhav_functions import DataHarvester as dhav
from initialization import Initializer as int_constructor

if __name__ == "__main__":
    path = "../apis_access/"
    api1 = apic("yfinance",["bonds","comodities_future","index_funds"],0)
    api2 = apic("nomics",["crypto","currency"],100,path,True)

    dh = dhav([api1,api2])
    
    dh.start_updating()
    