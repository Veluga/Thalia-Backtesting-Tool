import sys
import os
import pandas as pd

sys.path.append("../..")
from Finda import FdMultiController


def return_asset_classes():

    basepath = "tickers/"
    array_list = []
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            entry = entry.replace("_tickers.csv", "")
            array_list.append(entry)

    return array_list


"""
    The following comments go from Intern to Wary Wizard.
    Can the Wary Wizard verify if what the intern is treating
    Finda in the way she deserves to be treated ?
    In addition to this people like comments, or so I heard.
"""
"""
    The Intern creates the database and then he connects to it.
"""

# ask if db exists first
# FdMultiController.fd_create('first_db')
conn = FdMultiController.fd_connect("first_db", "rw")

"""
    Look into the tickers folder and based on the tickers there
    create the list of asset classes
"""
asset_classes_list = []
asset_classes_list = return_asset_classes()

"""
    Create a pandas.DataFrame of the format:
    {Columns: [], Index: [AssetClassName<String>]}
    Insert one at a time.
"""


for entry in asset_classes_list:
    print(entry)

data_frame_asset_classes = pd.DataFrame({"Columns": [], "Index": "index_funds"})

conn.write.write_asset_classes(data_frame_asset_classes)
