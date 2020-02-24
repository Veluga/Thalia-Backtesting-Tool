import pytest
import os
import sys

sys.path.append('../..')

from Harvester.DataHarvester.dhav_core.data_harvester import DataHarvester as dhorda
from Harvester.DataHarvester.dhav_core.initialization import Initializer as preulde_dhorda
from Harvester.DataHarvester.dhav_core.api_class import ApiObject as dhorda_api_warper

def test_get_data()
    