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


def asset_classes_list():
    basepath = "../tickers/"
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
'''
    register.db is missing what do I do now ?
'''
conn = FdMultiController.fd_connect("asset", "rw")

"""
    Look into the tickers folder and based on the tickers there
    create the list of asset classes
"""
asset_list = []
asset_list = asset_classes_list()

"""
    Create a pandas.DataFrame of the format:
    {Columns: [], Index: [AssetClassName<String>]}
    Insert all asset classes .

"""


data_frame_asset_class = pd.DataFrame(columns=[],index='AssetClassName')
conn.write.write_asset_classes(data_frame_asset_class)


