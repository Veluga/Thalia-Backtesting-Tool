import sys
import os
import pandas as pd
sys.path.append('../..')

from Harvester.DataHarvester.dhav_core.data_harvester import DataHarvester as dhorda

current_dir = os.path.dirname(__file__)

def test_interpolation():
    to_int = os.path.join(current_dir,"to_interpolate.csv")
    df_to_test = pd.read_csv(to_int)
    
    result = os.path.join(current_dir,"interpolation_result.csv")
    df_correct = pd.read_csv(result)
    
    dh = dhorda([])
    
    calculated_df = dh.add_interpolation_to_df(df_to_test)
    assert df_correct.equals(calculated_df)
    