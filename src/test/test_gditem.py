"""
    Testing GDItem class

    TODO:

    - non absolute
    - including .
    - including ..
    - including different number of steps in named_path and id_path
"""

import pytest
import gditem

def test_init_root():
    named_path = ['/']
    id_path = ['root']
    mime_type =  'application/vnd.google-apps.folder'
    item = gditem.GDItem(named_path, id_path, mime_type)

    assert item['name'] == '/'
    assert item['id'] == 'root'
    assert item['mimeType'] == 'application/vnd.google-apps.folder'
    assert item['namedPath'] == ['/']
    assert item['idPath'] == ['root']
    assert item.is_root()
    assert item.is_folder()

def test_method_root():
    item = gditem.GDItem.root()
    assert item['name'] == '/'
    assert item['id'] == 'root'
    assert item['mimeType'] == 'application/vnd.google-apps.folder'
    assert item['namedPath'] == ['/']
    assert item['idPath'] == ['root']
    assert item.is_root()
    assert item.is_folder()

def test_proper_item_folder():
    named_path = ['/', 'a', 'proper', 'path']
    id_path = ['root', 'aid', 'properid', 'pathid']
    mime_type =  'application/vnd.google-apps.folder'
    item = gditem.GDItem(named_path, id_path, mime_type)

    assert item['name'] == 'path'
    assert item['id'] == 'pathid'
    assert item['mimeType'] == 'application/vnd.google-apps.folder'
    assert item['namedPath'] == named_path
    assert item['idPath'] == id_path
    assert not item.is_root()
    assert item.is_folder()

def test_proper_method_folder():
    named_path = ['/', 'a', 'proper', 'path']
    id_path = ['root', 'aid', 'properid', 'pathid']
    item = gditem.GDItem.folder(named_path, id_path)
    assert item['name'] == 'path'
    assert item['id'] == 'pathid'
    assert item['mimeType'] == 'application/vnd.google-apps.folder'
    assert item['namedPath'] == named_path
    assert item['idPath'] == id_path
    assert not item.is_root()
    assert item.is_folder()


def test_proper_item_file():
    named_path = ['/', 'a', 'proper', 'file.jpg']
    id_path = ['root', 'aid', 'properid', 'fileid']
    mime_type =  'application/img.jpeg'
    item = gditem.GDItem(named_path, id_path, mime_type)

    assert item['name'] == 'file.jpg'
    assert item['id'] == 'fileid'
    assert item['mimeType'] == 'application/img.jpeg'
    assert item['namedPath'] == named_path
    assert item['idPath'] == id_path
    assert not item.is_root()
    assert not item.is_folder()

def test_non_absolute_path():
    named_path = ['a', 'relative', 'path']
    id_path = ['aid', 'relativeid', 'pathid']
    mime_type =  'application/vnd.google-apps.folder'
    with pytest.raises(AssertionError):
        gditem.GDItem(named_path, id_path, mime_type)

def test_non_normalitze_path_with_dot():
    named_path = ['/', 'a', '.', 'path']
    id_path = ['root', 'aid', 'dotid', 'pathid']
    mime_type =  'application/vnd.google-apps.folder'
    with pytest.raises(AssertionError):
        gditem.GDItem(named_path, id_path, mime_type)

def test_non_normalitze_path_with_parent():
    named_path = ['/', 'a', '..', 'path']
    id_path = ['root', 'aid', 'dotdotid', 'pathid']
    mime_type =  'application/vnd.google-apps.folder'
    with pytest.raises(AssertionError):
        gditem.GDItem(named_path, id_path, mime_type)

def test_named_path_with_two_root():
    named_path = ['/', 'one', '/', 'two']
    id_path = ['root', 'oneid', 'root2', 'two']
    mime_type =  'application/vnd.google-apps.folder'
    with pytest.raises(AssertionError):
        gditem.GDItem(named_path, id_path, mime_type)

def test_named_path_with_two_root():
    named_path = ['/', 'one', '/thisisvalid!', 'two']
    id_path = ['root', 'oneid', 'root', 'two']
    mime_type =  'application/vnd.google-apps.folder'
    with pytest.raises(AssertionError):
        gditem.GDItem(named_path, id_path, mime_type)


def test_full_path_when_root():
    item = gditem.GDItem.root()
    expected = '/'
    got = item.full_path()
    assert got == expected

def test_full_path_when_non_root():
    item = gditem.GDItem.folder(['/', 'folder'], ['root', 'folderid'])
    expected = '/folder'
    got = item.full_path()
    assert got == expected
