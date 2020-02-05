# configure pytest

import os
import pytest

@pytest.fixture(scope="session")
def db_controller():
    ''' return db controller for use with testing
    '''
    FdMultiController.fd_create('__test_db__')
    yield FdMultiController.fd_connect('__test_db__', 'rwd')
    FdMultiController.fd_remove('__test_db__')

