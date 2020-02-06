# configure pytest

import os
import pytest
from Finda import FdMultiController


def clear_DBs():
    #remove all financial database for testing environment
    for ndb in FdMultiController.fd_list():
        FdMultiController.fd_remove(ndb)

@pytest.fixture(scope="function")
def db_controller():
    ''' return db controller for use with testing
    '''
    clear_DBs()
    FdMultiController.fd_create('__test_db__')
    yield FdMultiController.fd_connect('__test_db__', 'rwd')
    clear_DBs()
