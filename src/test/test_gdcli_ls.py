"""
    Testing of gdcli_ls utilities
    This module is expected to be run by pytest

    TODO:

        path is a existing file
        path is a existing folder
        path is a non existing file/folder
        path contains a non existing step
"""

import pytest
import gdcore
import gdstatus
import gdcli_ls
import utiltests

@pytest.fixture()
def initial_pwd_root(monkeypatch):
    contents = {
        'pwd': [ '' ],
        'pwd_id': ['root']
    }
    monkeypatch.setattr(gdstatus, 'get_status', lambda: contents)

@pytest.fixture()
def initial_pwd_non_root(monkeypatch):
    contents = {
        'pwd': ['', 'granpafolder', 'parentfolder', 'currentfolder'],
        'pwd_id': ['root', 'granpafolderid', 'parentfolderid', 'currentfolderid']
    }
    monkeypatch.setattr(gdstatus, 'get_status', lambda: contents)

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
        [ {'name': 'file1', 'id': 'id1',
         'mimeType': 'application/vnd.google-apps.folder'},
        {'name': 'file2', 'id': 'id2',
         'mimeType': 'application/vnd.google-apps.folder'},],
    ]
    fake_get_list = utiltests.build_mock_get(contents)
    monkeypatch.setattr(gdcore, 'get_list', fake_get_list)
    files, error_message = gdcli_ls.get_files(path)
    assert contents[0] == files
    assert '' == error_message

def test_ls_get_files_path_is_existing_file(monkeypatch):
    path = '/granpafolder/parentfolder/currentfolder/file1.jpg'
    contents_file = [
        [
            {'name': 'granpafolder', 'id': 'granpafolderid',
             'mimeType': 'application/vnd.google-apps.folder'}
        ],
        [
            {'name': 'parentfolder', 'id': 'parentfolderid',
             'mimeType': 'application/vnd.google-apps.folder'},
         ],
        [
            {'name': 'currentfolder', 'id': 'currentfolderid',
             'mimeType': 'application/vnd.google-apps.folder'},
         ],
        [ {'name': 'file1.jpg', 'id': 'file1id',
           'mimeType': 'image/jpeg'}],
    ]
    contents_list = []

    fake_get_file = utiltests.build_mock_get(contents_file)
    monkeypatch.setattr(gdcore, 'get_file', fake_get_file)
    fake_get_list = utiltests.build_mock_get(contents_list)
    monkeypatch.setattr(gdcore, 'get_list', fake_get_list)
    files, error_message = gdcli_ls.get_files(path)
    assert [] == files
    assert '' == error_message

