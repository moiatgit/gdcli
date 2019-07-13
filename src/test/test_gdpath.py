"""
    Testing of gdpath utilities
    This module is expected to be run by pytest
"""
import pytest
import gdcore
import gdstatus
import gditem
import gdpath
import utiltests


# fixtures and helping functions

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
        'pwd':    ['/', 'folder_a', 'folder_b', 'folder_c'],
        'pwd_id': ['root', 'folder_a_id', 'folder_b_id', 'folder_c_id']
    }
    monkeypatch.setattr(gdstatus, 'get_status', lambda: contents)

def assert_expected_results(contents, path, expected_items, monkeypatch):
    """ given the contents to be return by the GD API and
        the path to query and
        the expected items to be found, it
        asserts that the items found in GD for this path are the expected ones
    """
    fake_get_items_by_name = utiltests.build_mock_get(contents)
    monkeypatch.setattr(gdcore, 'get_items_by_name', fake_get_items_by_name)

    items = gdpath.items_from_path(path)
    assert items == expected_items


# test split_nixpath()

def test_split_nixpath_with_backslash():
    nixpath = 'sla\\\\sh'
    expected = ['sla\\sh']
    found = gdpath.split_nixpath(nixpath)
    assert found == expected

def test_split_nixpath_with_slash():
    nixpath = 'sla\\/sh'
    expected = ['sla/sh']
    found = gdpath.split_nixpath(nixpath)
    assert found == expected

def test_split_nixpath_root():
    nixpath = '/'
    expected = ['/']
    found = gdpath.split_nixpath(nixpath)
    assert found == expected

def test_split_nixpath_empty():
    nixpath = ''
    expected = ['']
    found = gdpath.split_nixpath(nixpath)
    assert found == expected

def test_split_nixpath_relative():
    nixpath = 'one/two/three'
    expected = ['one', 'two', 'three']
    found = gdpath.split_nixpath(nixpath)
    assert found == expected

def test_split_nixpath_aberrant():
    nixpath = '/a/very\\/aber..rant/pat\\\\h/isn\'t it?'
    expected = ['/', 'a', 'very/aber..rant', 'pat\\h', 'isn\'t it?']
    found = gdpath.split_nixpath(nixpath)
    assert found == expected

def test_split_nixpath_slash_parent():
    nixpath = '/..'
    expected = ['/', '..']
    found = gdpath.split_nixpath(nixpath)
    assert found == expected

# tst normalize_splitted_path()

def test_normalize_splitted_path_basic():
    path = ['one', 'two', 'three']
    expected = path
    found = gdpath.normalize_splitted_path(path)
    assert found == expected

def test_normalize_splitted_path_ignore_dot():
    path = ['.', 'one', '.', 'two.', '.three', '.']
    expected = ['one', 'two.', '.three']
    found = gdpath.normalize_splitted_path(path)
    assert found == expected

def test_normalize_splitted_path_ignore_dotdot():
    path = ['one', 'two', '..', 'three']
    expected = ['one', 'three']
    found = gdpath.normalize_splitted_path(path)
    assert found == expected

def test_normalize_splitted_path_preserve_initial_dotdot():
    path = ['..', 'one', '..', '..', 'two', '..', '..', 'three']
    expected = ['..', '..', '..', 'three']
    found = gdpath.normalize_splitted_path(path)
    assert found == expected

def test_normalize_splitted_path_dotdot_removing_all_path():
    path = ['one', 'two', 'three', '..', '..', '..', '..']
    expected = ['..']
    found = gdpath.normalize_splitted_path(path)
    assert found == expected

def test_normalize_splitted_path_only_one_dot():
    path = ['.']
    expected = ['']
    found = gdpath.normalize_splitted_path(path)
    assert found == expected

def test_normalize_splitted_path_only_dots():
    path = ['.', '.', '.', '.', '.', '.']
    expected = ['']
    found = gdpath.normalize_splitted_path(path)
    assert found == expected

def test_normalize_splitted_path_slash_parent():
    path = ['/', '..']
    expected = ['/']
    found = gdpath.normalize_splitted_path(path)
    assert found == expected

def test_normalize_splitted_path_slash_multiple_parent():
    path = ['/', '..', '..', '..']
    expected = ['/']
    found = gdpath.normalize_splitted_path(path)
    assert found == expected

def test_normalize_splitted_path_dot_dotdot():
    path = ['.', '..']
    expected = ['..']
    found = gdpath.normalize_splitted_path(path)
    assert found == expected

def test_normalize_splitted_path_slash_dot_dotdot():
    path = ['/', '.', '..']
    expected = ['/']
    found = gdpath.normalize_splitted_path(path)
    assert found == expected


# test items_from_path()

def test_path_slash_when_on_root(initial_pwd_root):
    path = '/'
    expected_item = gditem.GDItem.root()
    items = gdpath.items_from_path(path)
    assert len(items) == 1
    assert items[0] == expected_item


def test_path_slash_when_not_on_root(initial_pwd_non_root):
    path = '/'
    expected_item = gditem.GDItem.root()
    items = gdpath.items_from_path(path)
    assert len(items) == 1
    assert items[0] == expected_item


def test_path_non_existing_relative_item_from_root(monkeypatch, initial_pwd_root):
    path = 'nonexistentfile'
    contents = [[]]
    fake_get_items_by_name = utiltests.build_mock_get(contents,
                                             expected_args=('nonexistentfile',),
                                             expected_kwargs={'folder': gditem.GDItem.root()})
    monkeypatch.setattr(gdcore, 'get_items_by_name', fake_get_items_by_name)
    items = gdpath.items_from_path(path)
    assert not items


def test_path_non_existing_absolute_item_from_root(monkeypatch, initial_pwd_root):
    path = '/nonexistentfile'
    contents = [[]]
    fake_get_items_by_name = utiltests.build_mock_get(contents,
                                             expected_args=('nonexistentfile',),
                                             expected_kwargs={'folder': gditem.GDItem.root()})
    monkeypatch.setattr(gdcore, 'get_items_by_name', fake_get_items_by_name)
    items = gdpath.items_from_path(path)
    assert not items

def test_path_non_existing_relative_item_from_non_root(monkeypatch, initial_pwd_non_root):
    path = 'nonexistentfile'
    contents = [[]]
    named_path = ['/', 'folder_a', 'folder_b', 'folder_c']
    id_path = ['root', 'folder_a_id', 'folder_b_id', 'folder_c_id']
    expected_folder = gditem.GDItem.folder(named_path, id_path)
    fake_get_items_by_name = utiltests.build_mock_get(contents,
                                             expected_args=('nonexistentfile',),
                                             expected_kwargs={'folder': expected_folder})
    monkeypatch.setattr(gdcore, 'get_items_by_name', fake_get_items_by_name)
    items = gdpath.items_from_path(path)
    assert not items


def test_path_non_existing_absolute_item_from_non_root(monkeypatch, initial_pwd_non_root):
    path = '/nonexistentfile'
    contents = [[]]
    fake_get_items_by_name = utiltests.build_mock_get(contents,
                                             expected_args=('nonexistentfile',),
                                             expected_kwargs={'folder': gditem.GDItem.root()})
    monkeypatch.setattr(gdcore, 'get_items_by_name', fake_get_items_by_name)
    items = gdpath.items_from_path(path)
    assert not items


def test_path_slash_existent_folder_from_root(monkeypatch, initial_pwd_root):
    path = '/folder1'
    named_path = ['/', 'folder1']
    id_path = ['root', 'folder1id']
    contents = [[gditem.GDItem.folder(named_path, id_path)]]
    fake_get_items_by_name = utiltests.build_mock_get(contents)
    monkeypatch.setattr(gdcore, 'get_items_by_name', fake_get_items_by_name)
    expected_item = gditem.GDItem.folder(['/', 'folder1'], ['root', 'folder1id'])
    items = gdpath.items_from_path(path)
    assert len(items) == 1
    assert items[0] == expected_item


def test_path_dot_existent_folder_from_root(monkeypatch, initial_pwd_non_root):
    path = './folder1'
    named_path = ['/','folder_a','folder_b','folder_c','folder1']
    id_path = ['root', 'folder_a_id', 'folder_b_id', 'folder_c_id', 'folder1id']
    contents = [[gditem.GDItem.folder(named_path, id_path)]]
    expected_item = gditem.GDItem.folder( named_path, id_path)
    assert_expected_results(contents, path, [expected_item], monkeypatch)


def test_path_dot(initial_pwd_non_root):
    path = '.'
    named_path = ['/', 'folder_a','folder_b','folder_c']
    id_path = ['root', 'folder_a_id', 'folder_b_id', 'folder_c_id']
    expected_item = gditem.GDItem.folder(named_path, id_path)
    items = gdpath.items_from_path(path)
    assert len(items) == 1
    assert items[0] == expected_item


def test_path_dot_slash(initial_pwd_non_root):
    path = './'
    named_path = ['/', 'folder_a','folder_b','folder_c']
    id_path = ['root', 'folder_a_id', 'folder_b_id', 'folder_c_id']
    expected_item = gditem.GDItem.folder(named_path, id_path)
    items = gdpath.items_from_path(path)
    assert len(items) == 1
    assert items[0] == expected_item


def test_path_dot_slash_repeated(initial_pwd_non_root):
    path = '././././.'
    named_path = ['/', 'folder_a','folder_b','folder_c']
    id_path = ['root', 'folder_a_id', 'folder_b_id', 'folder_c_id']
    expected_item = gditem.GDItem.folder(named_path, id_path)
    items = gdpath.items_from_path(path)
    assert len(items) == 1
    assert items[0] == expected_item


def test_path_parent(initial_pwd_non_root):
    path = '..'
    named_path = ['/', 'folder_a','folder_b']
    id_path = ['root', 'folder_a_id', 'folder_b_id']
    expected_item = gditem.GDItem.folder(named_path, id_path)
    items = gdpath.items_from_path(path)
    assert len(items) == 1
    assert items[0] == expected_item


def test_path_parent_slash(initial_pwd_non_root):
    path = '../'
    named_path = ['/', 'folder_a','folder_b']
    id_path = ['root', 'folder_a_id', 'folder_b_id']
    expected_item = gditem.GDItem.folder(named_path, id_path)
    items = gdpath.items_from_path(path)
    assert len(items) == 1
    assert items[0] == expected_item


def test_path_parent_parent(initial_pwd_non_root):
    path = '../..'
    named_path = ['/', 'folder_a']
    id_path = ['root', 'folder_a_id']
    expected_item = gditem.GDItem.folder(named_path, id_path)
    items = gdpath.items_from_path(path)
    assert len(items) == 1
    assert items[0] == expected_item


def test_path_too_much_parents(initial_pwd_non_root):
    path = '../../../../..'
    expected_item = gditem.GDItem.root()
    items = gdpath.items_from_path(path)
    assert len(items) == 1
    assert items[0] == expected_item


def test_path_slash_parent(initial_pwd_non_root):
    path = '/..'
    expected_item = gditem.GDItem.root()
    items = gdpath.items_from_path(path)
    assert len(items) == 1
    assert items[0] == expected_item


def test_path_mixing_parents_and_dots(initial_pwd_non_root):
    path = './.././../.'
    named_path = ['/', 'folder_a']
    id_path = ['root', 'folder_a_id']
    expected_item = gditem.GDItem.folder(named_path, id_path)
    items = gdpath.items_from_path(path)
    assert len(items) == 1
    assert items[0] == expected_item


def test_path_parent_replacing_folder_in_pwd(monkeypatch, initial_pwd_non_root):
    path = './../newfolder/folder1'
    named_path1 = ['/', 'folder_a', 'folder_b', 'newfolder']
    id_path1 = ['root', 'folder_a_id', 'folder_b_id', 'newfolder_id']
    named_path2 = ['/', 'folder_a', 'folder_b', 'newfolder', 'folder1']
    id_path2 = ['root', 'folder_a_id', 'folder_b_id', 'newfolder_id', 'folder1id']
    contents = [
        [gditem.GDItem.folder(named_path1, id_path1)],
        [gditem.GDItem.folder(named_path2, id_path2)]]
    expected_item = gditem.GDItem.folder(named_path2, id_path2)
    assert_expected_results(contents, path, [expected_item], monkeypatch)


def test_path_parent_replacing_folder_in_path(monkeypatch, initial_pwd_non_root):
    path = './forgetfolder/.././../newfolder/folder1'
    named_path1 = ['/', 'folder_a', 'folder_b', 'newfolder']
    id_path1 = ['root', 'folder_a_id', 'folder_b_id', 'newfolder_id']
    named_path2 = ['/', 'folder_a', 'folder_b', 'newfolder', 'folder1']
    id_path2 = ['root', 'folder_a_id', 'folder_b_id', 'newfolder_id', 'folder1id']
    contents = [
        [gditem.GDItem.folder(named_path1, id_path1)],
        [gditem.GDItem.folder(named_path2, id_path2)]]
    expected_item = gditem.GDItem.folder(named_path2, id_path2)
    assert_expected_results(contents, path, [expected_item], monkeypatch)


def test_path_slash_existent_existent_folder(monkeypatch, initial_pwd_root):
    path = '/folder1/folder2'
    named_path1 = ['/', 'folder1']
    id_path1 = ['root', 'folder1id']
    named_path2 = ['/', 'folder1', 'folder2']
    id_path2 = ['root', 'folder1id', 'folder2id']
    contents = [
        [ gditem.GDItem.folder(named_path1, id_path1)],
        [ gditem.GDItem.folder(named_path2, id_path2)],
    ]
    expected_item = gditem.GDItem.folder(named_path2, id_path2)
    assert_expected_results(contents, path, [expected_item], monkeypatch)


def test_path_slash_existent_existent_file(monkeypatch, initial_pwd_root):
    path = '/folder1/file2.jpg'
    named_path1 = ['/', 'folder1']
    id_path1 = ['root', 'folder1id']
    named_path2 = ['/', 'folder1', 'file2.jpg']
    id_path2 = ['root', 'folder1id', 'file2jpgid']
    contents = [
        [ gditem.GDItem.folder(named_path1, id_path1)],
        [ gditem.GDItem.folder(named_path2, id_path2)],
    ]

    contents = [
        [ gditem.GDItem.folder(named_path1, id_path1) ],
        [ gditem.GDItem(named_path2, id_path2, 'image/jpeg') ]
    ]
    expected_item =  gditem.GDItem(named_path2, id_path2, 'image/jpeg')
    assert_expected_results(contents, path, [expected_item], monkeypatch)


def test_path_slash_existent_dot_parent(monkeypatch, initial_pwd_root):
    path = '/folder1/./..'
    contents = []
    expected_item = gditem.GDItem.root()
    assert_expected_results(contents, path, [expected_item], monkeypatch)


def test_path_slash_existent_nonexistent(monkeypatch, initial_pwd_root):
    path = '/folder1/nonexistentfile'
    named_path1 = ['/', 'folder1']
    id_path1 = ['root', 'folder1id']
    contents = [
        [gditem.GDItem.folder(named_path1, id_path1)],
        []
    ]
    assert_expected_results(contents, path, [], monkeypatch)


def test_path_existent_file_as_folder(monkeypatch, initial_pwd_root):
    path = '/img.jpg/anything'
    named_path2 = ['/', 'folder1', 'file2.jpg']
    id_path2 = ['root', 'folder1id', 'file2jpgid']
    contents = [
        [ gditem.GDItem(named_path2, id_path2, 'image/jpeg') ]
    ]
    assert_expected_results(contents, path, [], monkeypatch)


def test_path_more_than_one_file_with_same_name_in_same_folder(monkeypatch):
    contents = [
        [gditem.GDItem.folder('/folder1', ['root', 'folder1id'])],
        [gditem.GDItem('/folder1/img.jpg', ['root', 'folder1id', 'imgjpgid1'], 'image/jpeg'),
         gditem.GDItem('/folder1/img.jpg', ['root', 'folder1id', 'imgjpgid2'], 'image/jpeg')]
    ]
    path = '/folder1/img.jpg'
    expected_items = [
        gditem.GDItem('/folder1/img.jpg', ['root', 'folder1id', 'imgjpgid1'], 'image/jpeg'),
        gditem.GDItem('/folder1/img.jpg', ['root', 'folder1id', 'imgjpgid2'], 'image/jpeg')
    ]
    assert_expected_results(contents, path, expected_items, monkeypatch)


def test_path_two_folders_with_same_name_one_with_required_file_and_the_other_without(monkeypatch):
    contents = [
        [
            gditem.GDItem.folder('/folder1', ['root', 'folder1id1']),
            gditem.GDItem.folder('/folder1', ['root', 'folder1id2']),
        ],
        [gditem.GDItem('/folder1/img1.jpg', ['root', 'folder1id1', 'img1jpgid'], 'image/jpeg')],
        [],
    ]
    path = '/folder1/img1.jpg'
    expected_items = [
        gditem.GDItem('/folder1/img1.jpg', ['root', 'folder1id1', 'img1jpgid'], 'image/jpeg')
    ]
    assert_expected_results(contents, path, expected_items, monkeypatch)


def test_path_two_folders_with_same_name_both_with_required_file(monkeypatch):
    contents = [
        [
            gditem.GDItem.folder('/folder1', ['root', 'folder1id1']),
            gditem.GDItem.folder('/folder1', ['root', 'folder1id2']),
        ],
        [gditem.GDItem('/folder1/img1.jpg', ['root', 'folder1id1', 'img1jpgid1'], 'image/jpeg')],
        [gditem.GDItem('/folder1/img1.jpg', ['root', 'folder1id2', 'img1jpgid2'], 'image/jpeg')],
    ]
    path = '/folder1/img1.jpg'
    expected_items = [
        gditem.GDItem('/folder1/img1.jpg', ['root', 'folder1id1', 'img1jpgid1'], 'image/jpeg'),
        gditem.GDItem('/folder1/img1.jpg', ['root', 'folder1id2', 'img1jpgid2'], 'image/jpeg')
    ]
    assert_expected_results(contents, path, expected_items, monkeypatch)


def test_path_a_file_and_a_folder_with_same_name_is_same_folder(monkeypatch):
    contents = [
        [ gditem.GDItem.folder('/folder1', ['root', 'folder1id'])],
        [
            gditem.GDItem('/folder1/theitem', ['root', 'folder1id', 'theitemid1'], 'image/jpeg'),
            gditem.GDItem.folder('/folder1/theitem', ['root', 'folder1id', 'theitemid2']),
        ]
    ]
    path = '/folder1/theitem'
    expected_items = [
            gditem.GDItem('/folder1/theitem', ['root', 'folder1id', 'theitemid1'], 'image/jpeg'),
            gditem.GDItem.folder('/folder1/theitem', ['root', 'folder1id', 'theitemid2']),
    ]
    assert_expected_results(contents, path, expected_items, monkeypatch)


def test_path_same_name_step_one_a_file_the_other_a_folder_containing_expected(monkeypatch):
    contents = [
        [
            gditem.GDItem('/theitem', ['root', 'theitemid1'], 'image/jpeg'),
            gditem.GDItem.folder('/theitem', ['root', 'theitemid2']),
        ],
        [gditem.GDItem('/theitem/img.jpg', ['root', 'theitemid2', 'imgjpgid'], 'image/jpeg'),]
    ]
    path = '/theitem/img.jpg'
    expected_items = [
            gditem.GDItem('/theitem/img.jpg', ['root', 'theitemid2', 'imgjpgid'], 'image/jpeg'),
    ]
    assert_expected_results(contents, path, expected_items, monkeypatch)


