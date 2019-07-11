"""
    Testing of gdpath utilities
    This module is expected to be run by pytest

    TODO tests

    /nonexistent/..
    /existingfile/something

"""
import pytest
import gdcore
import gdstatus
import gditem
import gdpath
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
        'pwd':     '/granpafolder/parentfolder/currentfolder',
        'pwd_id': ['root', 'granpafolderid', 'parentfolderid', 'currentfolderid']
    }
    print("XXX YYY initial pwd", contents)
    monkeypatch.setattr(gdstatus, 'get_status', lambda: contents)


def test_path_slash_when_on_root(initial_pwd_root):
    given = '/'
    obtained_item, error_message = gdpath.named_path_to_gd_item(given)
    expected_item = gditem.GDItem.root()
    assert obtained_item == expected_item
    assert len(error_message) == 0


def test_path_slash_when_not_on_root(initial_pwd_non_root):
    given = '/'
    obtained_item, error_message = gdpath.named_path_to_gd_item(given)
    expected_item = gditem.GDItem.root()
    assert obtained_item == expected_item
    assert len(error_message) == 0


def test_path_non_existing(monkeypatch, initial_pwd_root):
    contents = []

    def fake_get_file(filename, folder=None):
        print("XXX fake_get_file(filename: %s, folder: %s)" % (filename, folder))
        assert folder == 'root'
        assert filename == 'nonexistentfile'
        return contents

    monkeypatch.setattr(gdcore, 'get_file', fake_get_file)
    given = 'nonexistentfile'
    path_id, error_message = gdpath.named_path_to_gd_item(given)
    expected_item = None
    expected_msg = 'not found: %s' % given
    assert expected_item == path_id
    assert expected_msg == error_message


def test_path_dot_non_existing(monkeypatch, initial_pwd_root):
    contents = []

    def fake_get_file(filename, folder=None):
        assert folder == 'root'
        assert filename == 'nonexistentfile'
        return contents

    monkeypatch.setattr(gdcore, 'get_file', fake_get_file)
    given = '/nonexistentfile'
    path_id, error_message = gdpath.named_path_to_gd_item(given)
    expected_item = None
    expected_msg = 'not found: nonexistentfile'
    assert expected_item == path_id
    assert expected_msg == error_message


def test_path_slash_existent_folder_from_root(monkeypatch, initial_pwd_root):
    contents = [
        [gditem.GDItem.folder('/folder1', ['root', 'folder1id'])]
    ]
    fake_get_file = utiltests.build_mock_get(contents)
    monkeypatch.setattr(gdcore, 'get_file', fake_get_file)
    given = '/folder1'
    path_id, error_message = gdpath.named_path_to_gd_item(given)
    expected_item = gditem.GDItem.folder('/folder1', ['root', 'folder1id'])
    expected_msg = ''
    assert expected_item == path_id
    assert expected_msg == error_message


def test_path_dot_existent_folder_from_root(monkeypatch, initial_pwd_non_root):
    contents = [[
        gditem.GDItem.folder('/granpafolder/parentfolder/currentfolder/folder1',
                             ['root', 'granpafolderid', 'parentfolderid',
                              'currentfolderid', 'folder1id'])]]
    fake_get_file = utiltests.build_mock_get(contents)
    monkeypatch.setattr(gdcore, 'get_file', fake_get_file)
    given = './folder1'
    path_id, error_message = gdpath.named_path_to_gd_item(given)
    expected_item = gditem.GDItem.folder(
        '/granpafolder/parentfolder/currentfolder/folder1',
        ['root', 'granpafolderid', 'parentfolderid',
         'currentfolderid', 'folder1id']
    )
    expected_msg = ''
    assert expected_item == path_id
    assert expected_msg == error_message


def test_path_dot(initial_pwd_non_root):
    given = '.'
    path_id, error_message = gdpath.named_path_to_gd_item(given)
    expected_item = gditem.GDItem.folder('/granpafolder/parentfolder/currentfolder',
                                         ['root', 'granpafolderid', 'parentfolderid', 'currentfolderid'])
    expected_msg = ''
    assert expected_item == path_id
    assert expected_msg == error_message


def test_path_dot_slash(initial_pwd_non_root):
    given = './'
    path_id, error_message = gdpath.named_path_to_gd_item(given)
    expected_item = gditem.GDItem.folder('/granpafolder/parentfolder/currentfolder',
                                         ['root', 'granpafolderid', 'parentfolderid', 'currentfolderid'])
    expected_msg = ''
    assert expected_item == path_id
    assert expected_msg == error_message


def test_path_dot_slash_repeated(initial_pwd_non_root):
    given = '././././.'
    path_id, error_message = gdpath.named_path_to_gd_item(given)
    expected_item = gditem.GDItem.folder('/granpafolder/parentfolder/currentfolder',
                                         ['root', 'granpafolderid', 'parentfolderid', 'currentfolderid'])
    expected_msg = ''
    assert expected_item == path_id
    assert expected_msg == error_message


def test_path_parent(initial_pwd_non_root):
    given = '..'
    path_id, error_message = gdpath.named_path_to_gd_item(given)
    expected_item = gditem.GDItem.folder('/granpafolder/parentfolder',
                                         ['root', 'granpafolderid', 'parentfolderid'])
    expected_msg = ''
    assert expected_item == path_id
    assert expected_msg == error_message


def test_path_parent_slash(initial_pwd_non_root):
    given = '../'
    path_id, error_message = gdpath.named_path_to_gd_item(given)
    expected_item = 'parentfolderid'
    expected_msg = ''
    assert expected_item == path_id
    assert expected_msg == error_message


def test_path_parent_parent(initial_pwd_non_root):
    given = '../..'
    path_id, error_message = gdpath.named_path_to_gd_item(given)
    expected_item = 'granpafolderid'
    expected_msg = ''
    assert expected_item == path_id
    assert expected_msg == error_message


def test_path_slash_parent(initial_pwd_non_root):
    given = '/..'
    path_id, error_message = gdpath.named_path_to_gd_item(given)
    expected_item = 'root'
    expected_msg = ''
    assert expected_item == path_id
    assert expected_msg == error_message


def test_path_mixing_parents_and_dots(initial_pwd_non_root):
    given = './.././../.'
    path_id, error_message = gdpath.named_path_to_gd_item(given)
    expected_item = 'granpafolderid'
    expected_msg = ''
    assert expected_item == path_id
    assert expected_msg == error_message


def test_path_slash_existent_existent_folder(monkeypatch, initial_pwd_root):
    contents = [
        [ {'name': 'folder1', 'id': 'id1',
           'mimeType': 'application/vnd.google-apps.folder'}],
        [ {'name': 'folder2', 'id': 'id2',
           'mimeType': 'application/vnd.google-apps.folder'}],
    ]

    fake_get_file = utiltests.build_mock_get(contents)
    monkeypatch.setattr(gdcore, 'get_file', fake_get_file)
    given = '/folder1/folder2'
    path_id, error_message = gdpath.named_path_to_gd_item(given)
    expected_item = 'id2'
    expected_msg = ''
    assert expected_item == path_id
    assert expected_msg == error_message


def test_path_slash_existent_existent_file(monkeypatch, initial_pwd_root):
    contents = [
        [ {'name': 'folder1', 'id': 'id1',
           'mimeType': 'application/vnd.google-apps.folder'}],
        [ {'name': 'file2.jpg', 'id': 'id2',
           'mimeType': 'image/jpeg'}],
    ]

    fake_get_file = utiltests.build_mock_get(contents)
    monkeypatch.setattr(gdcore, 'get_file', fake_get_file)
    given = '/folder1/file2.jpg'
    path_id, error_message = gdpath.named_path_to_gd_item(given)
    expected_item = 'id2'
    expected_msg = ''
    assert expected_item == path_id
    assert expected_msg == error_message


def test_path_slash_existent_dot_parent(monkeypatch, initial_pwd_root):
    contents = [
        [ {'name': 'folder1', 'id': 'id1',
           'mimeType': 'application/vnd.google-apps.folder'}],
    ]

    fake_get_file = utiltests.build_mock_get(contents)
    monkeypatch.setattr(gdcore, 'get_file', fake_get_file)
    given = '/folder1/./..'
    path_id, error_message = gdpath.named_path_to_gd_item(given)
    expected_item = 'root'
    expected_msg = ''
    assert expected_item == path_id
    assert expected_msg == error_message


def test_path_slash_existent_nonexistent(monkeypatch, initial_pwd_root):
    contents = [
        [ {'name': 'folder1', 'id': 'id1',
           'mimeType': 'application/vnd.google-apps.folder'}],
        [],
    ]

    fake_get_file = utiltests.build_mock_get(contents)
    monkeypatch.setattr(gdcore, 'get_file', fake_get_file)
    given = '/folder1/nonexistentfile'
    path_id, error_message = gdpath.named_path_to_gd_item(given)
    expected_item = ''
    expected_msg = 'not found: nonexistentfile'
    assert expected_item == path_id
    assert expected_msg == error_message


def test_path_existent_file_as_folder(monkeypatch, initial_pwd_root):
    contents = [
        [ {'name': 'img.jpg', 'id': 'id1',
           'mimeType': 'image/jpeg'}],
    ]

    fake_get_file = utiltests.build_mock_get(contents)
    monkeypatch.setattr(gdcore, 'get_file', fake_get_file)
    given = '/img.jpg/anything'
    path_id, error_message = gdpath.named_path_to_gd_item(given)
    expected_item = ''
    expected_msg = 'not a directory: img.jpg'
    assert expected_item == path_id
    assert expected_msg == error_message


