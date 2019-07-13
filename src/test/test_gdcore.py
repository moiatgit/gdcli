"""
    Testing of gdcore
    This module is expected to be run by pytest
"""

import pytest

import utiltests
import gdcore
import gditem

def test_items_by_name_one_hit(monkeypatch):
    name = 'theitem'
    folder = gditem.GDItem.root()
    contents = [
        { 'files': [
            { 'name': 'theitem', 'id':'theitemid', 'mimeType':'application/vnd.google-apps.folder' }
        ]} ,
    ]
    expected_items = [
        gditem.GDItem.folder('/theitem', ['root', 'theitemid']),
    ]
    expected_query = "name='theitem' and 'root' in parents and trashed=false"
    fake_get_raw_items = utiltests.build_mock_get(contents, expected_args=(expected_query,))
    monkeypatch.setattr(gdcore, '_get_raw_items', fake_get_raw_items)
    items = gdcore.get_items_by_name(name, folder)
    print("XXX items", items)
    print("XXX expected_items", expected_items)
    assert items == expected_items


