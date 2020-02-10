"""
Test for the fd_manager submodule of finda
"""

import pytest
from Finda import FdMultiController, fd_read, fd_write, fd_remove
from unittest import mock
import os


def test_fd_manager_fd_list(db_controller):
    assert "__seeded_test_db__" in FdMultiController.fd_list(), "failed to \
                                                                 register test db"
    # remove file and try to open
    os.remove(FdMultiController._path_generator("registered"))
    assert FdMultiController.fd_list() == [], "failed to remove db registry"


def test_fd_manager_fd_create(db_controller):
    # normal flow of events
    assert FdMultiController.fd_create("testDB1") is True, "reported faliure"
    assert "testDB1" in FdMultiController.fd_list()
    # given name already registered
    with pytest.raises(Exception) as e:
        FdMultiController.fd_create("testDB1")
        assert "already exists" in str(e.value), "incorrect exception raised"
    # DBsqlite3.OperationalError cannot be created
    assert FdMultiController.fd_create("/") is False, "created ivalid file /"
    with mock.patch("Finda.FdMultiController.fd_create") as m:
        m.side_effect = OSError
        with pytest.raises(OSError) as e:
            assert FdMultiController.fd_create() == "Hello World"
            pytest.fail("expected error creating uncreatable bd")


def test_fd_manager_fd_remove(db_controller):
    assert "__seeded_test_db__" in FdMultiController.fd_list(), "db not created"
    FdMultiController.fd_remove("__seeded_test_db__")
    assert FdMultiController.fd_list() == ["__empty_test_db__"], "error checking \
removed database removed from register"

def test_fd_manager_fd_connect(db_controller):
    # standard path; connect to valid database
    connRead = FdMultiController.fd_connect("__seeded_test_db__", "zzrzz")
    connWrite = FdMultiController.fd_connect("__seeded_test_db__", "zzwzz")
    connDelete = FdMultiController.fd_connect("__seeded_test_db__", "zzdzz")
    connMulti = FdMultiController.fd_connect("__seeded_test_db__", "zrzdzzw")

    # checking permissions
    assert type(connRead.read) == fd_read.FdRead, "error composing FdRead object \
to connection"
    assert type(connWrite.write) == fd_write.FdWrite, "error composing FdWrite \
object to connection"
    assert type(connDelete.remove) == fd_remove.FdRemove, "error composing \
FdRemove object to connection"
    assert connRead.write is None and connRead.remove is None, "error while \
checking only correct permissions were added"
    assert connWrite.read is None and connWrite.remove is None, "error while \
checking only correct permissions were added"
    assert connDelete.read is None and connDelete.write is None, "error while \
checking only correct permissions were added"
    assert (
        type(connMulti.read) == fd_read.FdRead
        and type(connMulti.write) == fd_write.FdWrite
        and type(connMulti.remove) == fd_remove.FdRemove
    )
    with pytest.raises(Exception):
        FdMultiController.fd_connect("RaNdOmGibBeRiSh", "rwd")
        pytest.fail("expected error connecting to non existent database")
