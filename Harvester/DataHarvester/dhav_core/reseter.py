'''
    Script for reseting the persitant_data 
'''

from initialization import Initializer as int_constructor
from api_class import ApiCaller as apic

if __name__ == "__main__":
    api1 = apic("yfinance", ["bonds", "comodities_future", "index_funds"], 10)
    api2 = apic("nomics", ["crypto", "currency"], 0, True)

    initer = int_constructor([api1, api2])
    initer.construct_circular_list()
    initer.construct_position()

