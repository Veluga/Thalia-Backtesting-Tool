import sys
sys.path.append('../..')
from  Finda import FdMultiController
import pandas as pd

'''

'''
FdMultiController.fd_create('first_db')
conn = FdMultiController.fd_connect('first_db', 'rw')


retrieved = conn.write.write_asset_classes()