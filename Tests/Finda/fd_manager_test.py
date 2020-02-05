'''
Test for the fd_manager submodule of finda
'''

import pytest
from Finda import FdMultiController


def fd_manager_fd_create_test():
    assert False
    #normal flow of events
    assert FdMultiController.db_create('testDB1') == True
    #given name already registered
    with pytest.raises(Exception, match="DB already exists"):
        FdMultiController.db_create('testDB1')
    ##DB cannot be created
    assert FdMultiController.db_create('/') == False
