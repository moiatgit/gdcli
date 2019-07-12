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
import gditem
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
        'pwd':     '/folder_a/folder_b/folder_c',
        'pwd_id': ['root', 'folder_a_id', 'folder_b_id', 'folder_c_id']
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
    contents_by_folder = [
        [
            gditem.GDItem.folder('/folder1', ['root', 'folder1id']),
            gditem.GDItem.folder('/folder2', ['root', 'folder2id']),
        ]
    ]
    expected_items = [
            gditem.GDItem.folder('/folder1', ['root', 'folder1id']),
            gditem.GDItem.folder('/folder2', ['root', 'folder2id']),
    ]
    fake_get_items_by_folder = utiltests.build_mock_get(contents_by_folder)
    monkeypatch.setattr(gdcore, 'get_items_by_folder', fake_get_items_by_folder)
    items = gdcli_ls.get_files(path)
    assert items == expected_items


def test_ls_path_to_non_folder_file(monkeypatch):
    path = '/img.jpg'
    contents_by_name = [
        [gditem.GDItem('/img.jpg', ['root', 'imgjpgid'], 'image/jpeg')]
    ]
    expected_items = [
        gditem.GDItem('/img.jpg', ['root', 'imgjpgid'], 'image/jpeg')
    ]
    fake_get_items_by_name = utiltests.build_mock_get(contents_by_name)
    monkeypatch.setattr(gdcore, 'get_items_by_name', fake_get_items_by_name)
    items = gdcli_ls.get_files(path)
    assert items == expected_items

"""
    other tests
    - ls when it is a folder
    - ls when a folder and a file with same name
    - ls when two folders with same name

    test also the printing results
"""
