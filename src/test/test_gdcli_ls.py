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
        'pwd': ['/'],
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


def test_ls_absolute_path_root(monkeypatch, initial_pwd_root):
    path = '/'
    named_path1 = ['/', 'folder1']
    id_path1 = ['root', 'folder1id']
    named_path2 = ['/', 'folder2']
    id_path2 = ['root', 'folder2id']
    contents_by_folder = [
        [
            gditem.GDItem.folder(named_path1, id_path1),
            gditem.GDItem.folder(named_path2, id_path2),
        ]
    ]
    expected_items = [
            gditem.GDItem.folder(named_path1, id_path1),
            gditem.GDItem.folder(named_path2, id_path2),
    ]
    fake_get_items_by_folder = utiltests.build_mock_get(contents_by_folder)
    monkeypatch.setattr(gdcore, 'get_items_by_folder', fake_get_items_by_folder)
    items = gdcli_ls.get_files(path)
    assert items == expected_items


def test_ls_absolute_path_to_non_folder_file(monkeypatch, initial_pwd_root):
    path = '/img.jpg'
    named_path1 = ['/', 'img.jpg']
    id_path1 = ['root', 'imgjpgid']
    contents_by_name = [
        [gditem.GDItem(named_path1, id_path1, 'image/jpeg')]
    ]
    expected_items = [
        gditem.GDItem(named_path1, id_path1, 'image/jpeg')
    ]
    fake_get_items_by_name = utiltests.build_mock_get(contents_by_name)
    monkeypatch.setattr(gdcore, 'get_items_by_name', fake_get_items_by_name)
    items = gdcli_ls.get_files(path)
    assert items == expected_items


def test_ls_path_to_folder(monkeypatch, initial_pwd_root):
    path = 'folder1'
    named_path1 = ['/', 'folder1']
    id_path1 = ['root', 'folder1id']
    named_path2 = ['/', 'folder1', 'img.jpg']
    id_path2 = ['root', 'folder1id', 'imgjpgid1']
    named_path3 = ['/', 'folder1', 'folder2']
    id_path3 = ['root', 'folder1id', 'folder2id']
    contents_by_name = [
        [ gditem.GDItem.folder(named_path1, id_path1)],
    ]
    contents_by_folder = [
        [ gditem.GDItem(named_path2, id_path2, 'image/jpeg'),
          gditem.GDItem.folder(named_path3, id_path3)]
    ]
    expected_items = [
        gditem.GDItem(named_path2, id_path2, 'image/jpeg'),
        gditem.GDItem.folder(named_path3, id_path3)
    ]
    fake_get_items_by_name = utiltests.build_mock_get(contents_by_name)
    fake_get_items_by_folder = utiltests.build_mock_get(contents_by_folder)
    monkeypatch.setattr(gdcore, 'get_items_by_name', fake_get_items_by_name)
    monkeypatch.setattr(gdcore, 'get_items_by_folder', fake_get_items_by_folder)
    items = gdcli_ls.get_files(path)
    assert items == expected_items


def test_ls_folder_and_file_with_same_name(monkeypatch, initial_pwd_root):
    path = 'theitem'
    named_path1 = ['/', 'theitem']
    id_path1 = ['root', 'theitemid1']
    id_path2 = ['root', 'theitemid2']

    named_path3 = ['/', 'theitem', 'img1.jpg']
    id_path3 = ['root', 'theitemid1', 'img1jpgid']
    named_path4 = ['/', 'theitem', 'folder2']
    id_path4 = ['root', 'theitemid1', 'folder2id']
    contents_by_name = [
        [
            gditem.GDItem.folder(named_path1, id_path1),
            gditem.GDItem(named_path1, id_path2, 'image/jpeg')
        ],
    ]
    contents_by_folder = [
        [ gditem.GDItem(named_path3, id_path3, 'image/jpeg'),
          gditem.GDItem.folder(named_path4, id_path4)]
    ]
    expected_items = [
        gditem.GDItem(named_path1, id_path2, 'image/jpeg'),
        gditem.GDItem(named_path3, id_path3, 'image/jpeg'),
        gditem.GDItem.folder(named_path4, id_path4)
    ]
    fake_get_items_by_name = utiltests.build_mock_get(contents_by_name)
    fake_get_items_by_folder = utiltests.build_mock_get(contents_by_folder)
    monkeypatch.setattr(gdcore, 'get_items_by_name', fake_get_items_by_name)
    monkeypatch.setattr(gdcore, 'get_items_by_folder', fake_get_items_by_folder)
    items = gdcli_ls.get_files(path)
    assert set(items) == set(expected_items)


def test_ls_two_folders_with_same_name(monkeypatch, initial_pwd_root):
    path = 'thefolder'
    named_path1 = ['/', 'theitem']
    id_path1 = ['root', 'theitemid1']
    id_path2 = ['root', 'theitemid2']
    named_path3 = ['/', 'theitem', 'img1.jpg']
    id_path3 = ['root', 'theitemid1', 'img1jpgid']
    named_path4 = ['/', 'theitem', 'img2.jpg']
    id_path4 = ['root', 'theitemid2', 'img2jpgid']
    contents_by_name = [
        [
            gditem.GDItem.folder(named_path1, id_path1),
            gditem.GDItem.folder(named_path1, id_path2),
        ],
    ]
    contents_by_folder = [
        [gditem.GDItem(named_path3, id_path3, 'image/jpeg')],
        [gditem.GDItem(named_path4, id_path4, 'image/jpeg')],
    ]
    expected_items = [
        gditem.GDItem(named_path3, id_path3, 'image/jpeg'),
        gditem.GDItem(named_path4, id_path4, 'image/jpeg'),
    ]
    fake_get_items_by_name = utiltests.build_mock_get(contents_by_name)
    fake_get_items_by_folder = utiltests.build_mock_get(contents_by_folder)
    monkeypatch.setattr(gdcore, 'get_items_by_name', fake_get_items_by_name)
    monkeypatch.setattr(gdcore, 'get_items_by_folder', fake_get_items_by_folder)
    items = gdcli_ls.get_files(path)
    assert set(items) == set(expected_items)

def test_print_item_when_folder():
    named_path = ['/', 'one', 'folder']
    id_path = ['root', 'oneid', 'folderid']
    item = gditem.GDItem.folder(named_path, id_path)
    expected = '/one/folder/'
    got = gdcli_ls.item_to_str(item)
    assert got == expected

def test_print_item_when_unknown_type():
    named_path = ['/', 'one', 'item']
    id_path = ['root', 'oneid', 'itemid']
    item = gditem.GDItem(named_path, id_path, 'application/vnd.google-apps.unknown')
    expected = '/one/itemname'
    got = gdcli_ls.item_to_str(item)
    assert got == expected

