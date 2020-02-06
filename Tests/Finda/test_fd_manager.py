'''
Test for the fd_manager submodule of finda
'''

import pytest
from Finda import FdMultiController


def test_fd_manager_fd_list(db_controller):
    assert '__test_db__' in FdMultiController.fd_list()

def test_fd_manager_fd_create(db_controller):
    # normal flow of events
    assert FdMultiController.fd_create('testDB1') == True
    assert 'testDB1' in FdMultiController.fd_list()
    # given name already registered
    with pytest.raises(Exception) as e:
        FdMultiController.fd_create('testDB1')
    assert e.value
    # DB cannot be created
    assert FdMultiController.fd_create('/') == False

def test_fd_manager_fd_remove(db_controller):
    assert '__test_db__' in FdMultiController.fd_list()
    FdMultiController.fd_remove('__test_db__')
    assert FdMultiController.fd_list() == [] 
