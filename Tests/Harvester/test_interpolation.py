import sys
import os
import pandas as pd
sys.path.append('../..')

from DataHarvester.dhav_core.data_harvester import DataHarvester as dhorda

current_dir = os.path.dirname(__file__)

def test_interpolation():
    to_int = os.path.join(current_dir,"to_interpolate.csv")
    df_to_test = pd.read_csv(to_int,float_precision=None)
    df_to_test["ADate"] = [
            word.split("T")[0]
            for word in df_to_test["ADate"]
        ]

    df_to_test['ADate'] = df_to_test['ADate'].astype('datetime64[ns]')
    
    result = os.path.join(current_dir,"interpolation_result.csv")
    df_correct = pd.read_csv(result)
    
    dh = dhorda([])

    df_to_test["AHigh"] = pd.to_numeric(df_to_test["AHigh"])
    df_to_test["ALow"] = pd.to_numeric(df_to_test["ALow"])
    df_to_test["AOpen"] = pd.to_numeric(df_to_test["AOpen"])
    df_to_test["AClose"] = pd.to_numeric(df_to_test["AClose"])


    calculated_df = dh.add_interpolation_to_df(df_to_test)
    #print(calculated_df.dtypes)
    #print(calculated_df.head(5))
    
    #print(df_correct.head(5))
   
  
    assert df_correct.equals(calculated_df)
    