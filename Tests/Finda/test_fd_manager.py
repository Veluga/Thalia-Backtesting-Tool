"""
Test for the fd_manager submodule of finda
"""

import pytest
from Finda import FdMultiController, fd_read, fd_write, fd_remove
from unittest import mock
import os


def test_fd_manager_fd_list(db_controller):
    assert "__seeded_test_db__" in FdMultiController.fd_list()
    # remove file and try to open
    os.remove(FdMultiController._path_generator("registered"))
    assert FdMultiController.fd_list() == []


def test_fd_manager_fd_create(db_controller):
    # normal flow of events
    assert FdMultiController.fd_create("testDB1") is True
    assert "testDB1" in FdMultiController.fd_list()
    # given name already registered
    with pytest.raises(Exception) as e:
        FdMultiController.fd_create("testDB1")
        assert "already exists" in str(e.value)
    # DBsqlite3.OperationalError cannot be created
    assert FdMultiController.fd_create("/") is False
    with mock.patch("Finda.FdMultiController.fd_create") as m:
        m.side_effect = OSError
        with pytest.raises(OSError) as e:
            assert FdMultiController.fd_create() == "Hello World"


def test_fd_manager_fd_remove(db_controller):
    assert "__seeded_test_db__" in FdMultiController.fd_list()
    FdMultiController.fd_remove("__seeded_test_db__")
    assert FdMultiController.fd_list() == ["__empty_test_db__"]


def test_fd_manager_fd_connect(db_controller):
    # standard path; connect to valid database
    connRead = FdMultiController.fd_connect("__seeded_test_db__", "zzrzz")
    connWrite = FdMultiController.fd_connect("__seeded_test_db__", "zzwzz")
    connDelete = FdMultiController.fd_connect("__seeded_test_db__", "zzdzz")
    connMulti = FdMultiController.fd_connect("__seeded_test_db__", "zrzdzzw")

    # checking permissions
    assert type(connRead.read) == fd_read.FdRead
    assert type(connWrite.write) == fd_write.FdWrite
    assert type(connDelete.remove) == fd_remove.FdRemove
    assert connRead.write is None and connRead.remove is None
    assert connWrite.read is None and connWrite.remove is None
    assert connDelete.read is None and connDelete.write is None
    assert (
        type(connMulti.read) == fd_read.FdRead
        and type(connMulti.write) == fd_write.FdWrite
        and type(connMulti.remove) == fd_remove.FdRemove
    )
    with pytest.raises(Exception) as e:
        FdMultiController.fd_connect("RaNdOmGibBeRiSh", "rwd")

    assert "DB name not registered with FinData controller" in str(e.value)
