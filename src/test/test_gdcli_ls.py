"""
    Testing of gdcli_ls utilities
    This module is expected to be run by pytest

    TODO tests

    When one arg only
    - when no files found
    - when one file
    - when more than one file

    When multiple args
"""

import pytest
import gdcore
import gdstatus
import gdcli_ls

@pytest.fixture(autouse=True)
def initial_pwd(monkeypatch):
    contents = {
        'pwd': '/',
        'pwd_id': ['root']
    }
    monkeypatch.setattr(gdstatus, 'get_status', lambda: contents)

def test_ls_path_root(monkeypatch):
    path = '/'
    contents = [
        {'name': 'file1', 'id': 'id1',
         'mimeType': 'application/vnd.google-apps.folder'},
        {'name': 'file2', 'id': 'id2',
         'mimeType': 'application/vnd.google-apps.folder'},
    ]
    def fake_get_list(path):
        assert path == 'root'
        return contents
    monkeypatch.setattr(gdcore, 'get_list', fake_get_list)
    files, error_message = gdcli_ls.get_files(path)
    assert contents == files
    assert '' == error_message
