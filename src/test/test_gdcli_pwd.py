"""
    test of gdcli_pwd
"""


import pytest
import gdstatus
import gdcli_pwd
import gditem

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
        'pwd': '/parentfolder/currentfolder',
        'pwd_id': ['root', 'parentfolderid', 'currentfolderid']
    }
    monkeypatch.setattr(gdstatus, 'get_status', lambda: contents)


def test_pwd_when_root(initial_pwd_root):
    obtained = gdcli_pwd.get_pwd()
    expected = '/'
    assert expected == obtained

def test_pwd_when_non_root(initial_pwd_non_root):
    obtained = gdcli_pwd.get_pwd()
    expected = '/parentfolder/currentfolder'
    assert expected == obtained

def test_pwd_gditem_when_root(initial_pwd_root):
    obtained = gdcli_pwd.get_pwd_gditem()
    expected = gditem.GDItem.root()
    assert expected == obtained

def test_pwd_gditem_when_non_root(initial_pwd_non_root):
    obtained = gdcli_pwd.get_pwd_gditem()
    expected = gditem.GDItem.folder('/parentfolder/currentfolder',
                                    ['root', 'parentfolderid', 'currentfolderid'])
    assert expected == obtained

