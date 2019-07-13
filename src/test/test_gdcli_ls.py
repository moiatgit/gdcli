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
        'pwd': '/',
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


def test_ls_absolute_path_to_non_folder_file(monkeypatch, initial_pwd_root):
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


def test_ls_path_to_folder(monkeypatch, initial_pwd_root):
    path = 'folder1'
    contents_by_name = [
        [ gditem.GDItem.folder('/folder1', ['root', 'folder1id'])],
    ]
    contents_by_folder = [
        [ gditem.GDItem('/folder1/img1.jpg', ['root', 'folder1id', 'img1jpgid'], 'image/jpeg'),
          gditem.GDItem.folder('/folder1/folder2', ['root', 'folder1id', 'folder2id'])]
    ]
    expected_items = [
        gditem.GDItem('/folder1/img1.jpg', ['root', 'folder1id', 'img1jpgid'], 'image/jpeg'),
        gditem.GDItem.folder('/folder1/folder2', ['root', 'folder1id', 'folder2id'])
    ]
    fake_get_items_by_name = utiltests.build_mock_get(contents_by_name)
    fake_get_items_by_folder = utiltests.build_mock_get(contents_by_folder)
    monkeypatch.setattr(gdcore, 'get_items_by_name', fake_get_items_by_name)
    monkeypatch.setattr(gdcore, 'get_items_by_folder', fake_get_items_by_folder)
    items = gdcli_ls.get_files(path)
    assert items == expected_items


def test_ls_folder_and_file_with_same_name(monkeypatch, initial_pwd_root):
    path = 'theitem'
    contents_by_name = [
        [
            gditem.GDItem.folder('/theitem', ['root', 'theitemid1']),
            gditem.GDItem('/theitem', ['root', 'theitemid2'], 'image/jpeg')
        ],
    ]
    contents_by_folder = [
        [ gditem.GDItem('/theitem/img1.jpg', ['root', 'theitemid1', 'img1jpgid'], 'image/jpeg'),
          gditem.GDItem.folder('/theitem/folder2', ['root', 'theitemid1', 'folder2id'])]
    ]
    expected_items = [
        gditem.GDItem('/theitem', ['root', 'theitemid2'], 'image/jpeg'),
        gditem.GDItem('/theitem/img1.jpg', ['root', 'theitemid1', 'img1jpgid'], 'image/jpeg'),
        gditem.GDItem.folder('/theitem/folder2', ['root', 'theitemid1', 'folder2id'])
    ]
    fake_get_items_by_name = utiltests.build_mock_get(contents_by_name)
    fake_get_items_by_folder = utiltests.build_mock_get(contents_by_folder)
    monkeypatch.setattr(gdcore, 'get_items_by_name', fake_get_items_by_name)
    monkeypatch.setattr(gdcore, 'get_items_by_folder', fake_get_items_by_folder)
    items = gdcli_ls.get_files(path)
    assert set(items) == set(expected_items)


def test_ls_two_folders_with_same_name(monkeypatch, initial_pwd_root):
    path = 'thefolder'
    contents_by_name = [
        [
            gditem.GDItem.folder('/theitem', ['root', 'theitemid1']),
            gditem.GDItem.folder('/theitem', ['root', 'theitemid2']),
        ],
    ]
    contents_by_folder = [
        [ gditem.GDItem('/theitem/img1.jpg', ['root', 'theitemid1', 'img1jpgid'], 'image/jpeg')],
        [ gditem.GDItem('/theitem/img2.jpg', ['root', 'theitemid2', 'img2jpgid'], 'image/jpeg')],
    ]
    expected_items = [
        gditem.GDItem('/theitem/img1.jpg', ['root', 'theitemid1', 'img1jpgid'], 'image/jpeg'),
        gditem.GDItem('/theitem/img2.jpg', ['root', 'theitemid2', 'img2jpgid'], 'image/jpeg'),
    ]
    fake_get_items_by_name = utiltests.build_mock_get(contents_by_name)
    fake_get_items_by_folder = utiltests.build_mock_get(contents_by_folder)
    monkeypatch.setattr(gdcore, 'get_items_by_name', fake_get_items_by_name)
    monkeypatch.setattr(gdcore, 'get_items_by_folder', fake_get_items_by_folder)
    items = gdcli_ls.get_files(path)
    assert set(items) == set(expected_items)

# XXX to be reviewed: they probably require Session to be mocked
#def test_print_item_when_folder():
#    item = gditem.GDItem.folder('/one/folder', ['root', 'oneid', 'folderid'])
#    expected = '/one/folder/'
#    got = gdcli_ls.item_to_str(item)
#    assert got == expected
#
#def test_print_item_when_unknown_type():
#    item = gditem.GDItem('/one/itemname', ['root', 'oneid', 'itemnameid'],
#                         'application/vnd.google-apps.unknown')
#    expected = '/one/itemname'
#    got = gdcli_ls.item_to_str(item)
#    assert got == expected

