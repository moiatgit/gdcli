"""
    Testing of gdpath utilities
    This module is expected to be run by pytest

    TODO tests

    .
    /
    ./
    ./nonexistent
    nonexistent
    /nonexistent
    /existent
    ..
    /..
    /existent/..

"""
import gdcore
import gdpath

def test_path_root():
    given = '/'
    path_id, error_message = gdpath.path_to_gd(given)
    expected_id = 'root'
    assert expected_id == path_id
    assert len(error_message) == 0

def test_path_non_existing(monkeypatch):
    contents = [
        {'name': 'file1', 'id': 'id1',
         'mimeType': 'application/vnd.google-apps.folder'}
    ]
    def fake_get_list(*args, **kwargs):
        assert len(args) == 0
        assert 'folder' in kwargs
        assert kwargs['folder'] == 'root'
        return contents

    monkeypatch.setattr(gdcore, 'get_list', fake_get_list)
    given = 'nonexistentfile'
    path_id, error_message = gdpath.path_to_gd(given)
    expected_id = ''
    expected_msg = 'not found file or folder %s' % given
    assert expected_id == path_id

