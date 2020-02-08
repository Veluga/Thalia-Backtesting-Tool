import pandas_datareader as pdread
import pandas as pd
import matplotlib.pyplot as plt
from api_class import ApiCaller as apic
from dhav_functions import DataHarvester as dhav
from initialization import Initializer as int_constructor

if __name__ == "__main__":
    
    api1 = apic("yfinance",["bonds","comodities_future","index_funds"],130)
    api2 = apic("nomics",["crypto","currency"],130,True)
   
    dh = dhav([api1,api2])
    dh.start_updating()
    
    #dh.construct_circular_list()
    #print(dh.assets_supported_by_api("nomics"))
    #dh.current_index("")
    #dh.next_index("nomics")
    #print(some_data)
    #plt.show()
