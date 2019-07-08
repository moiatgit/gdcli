"""
    Testing of gdpath utilities
    This module is expected to be run by pytest

    TODO tests

    .
    ./
    ./nonexistent
    nonexistent
    /nonexistent
    /existent
    ..
    /..
    /existent/..
    /nonexistent/..
    /existingfile/something

"""
import pytest
import gdcore
import gdstatus
import gdpath

@pytest.fixture(autouse=True)
def initial_pwd(monkeypatch):
    contents = {
        'pwd': '/',
        'pwd_id': ['root']
    }
    monkeypatch.setattr(gdstatus, 'get_status', lambda: contents)


def test_path_root():
    given = '/'
    path_id, error_message = gdpath.path_to_gd(given)
    expected_id = 'root'
    assert expected_id == path_id
    assert len(error_message) == 0


def test_path_non_existing(monkeypatch):
    contents = []

    def fake_get_file(filename, folder=None):
        assert folder == 'root'
        assert filename == 'nonexistentfile'
        return contents

    monkeypatch.setattr(gdcore, 'get_file', fake_get_file)
    given = 'nonexistentfile'
    path_id, error_message = gdpath.path_to_gd(given)
    expected_id = ''
    expected_msg = 'element not found: %s' % given
    assert expected_id == path_id
    assert expected_msg == error_message


def test_path_existent_file_from_root(monkeypatch):
    contents = [
        {'name': 'file1', 'id': 'id1',
         'mimeType': 'application/vnd.google-apps.folder'}
    ]
    def fake_get_file(filename, folder=None):
        assert folder == 'root'
        assert filename == 'file1'
        return contents

    monkeypatch.setattr(gdcore, 'get_file', fake_get_file)
    given = '/file1'
    path_id, error_message = gdpath.path_to_gd(given)
    expected_id = 'id1'
    expected_msg = ''
    assert expected_id == path_id
    assert expected_msg == error_message
