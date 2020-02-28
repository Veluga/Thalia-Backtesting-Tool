import sys
import os
import pandas as pd
sys.path.append('../..')

from Harvester.DataHarvester.dhav_core.data_harvester import DataHarvester as dhorda


def test_interpolation():
    
    df_to_test = pd.read_csv("to_interpolate.csv")
    df_correct = pd.read_csv("interpolation_result.csv")
    
    dh = dhorda([])
    
    calculated_df = dh.add_interpolation_to_df(df_to_test)
    assert df_correct.equals(calculated_df)
    