"""
    Google Drive item

    This module includes an encapsulation of an item in Google Drive

    It behaves as a dict but includes some specific aiding functions
"""

import collections
import gdconstants

class GDItem(collections.UserDict):
    """ This class encapsulates a item in GD
        It behaves like a dict() with, at least, the following keys
        - name: item name
        - id:   item id at GD
        - mimeType: mime type as GD reported
        - named_path: str with the absolute path (by default '/')
        - id_path: list of ids of folders to reach the item (first is always 'root')
    """

    def __init__(self, named_path, id_path, mime_type):
        """ initializes a new instance of a GD item
            @param named_path: str *nix like absolute and normalized path to this item
                   i.e. named_path must start with '/' and contain not '.' nor '..' steps.
            @param id_path: list of Google Drive ids composing the path to this item
            @param mime_type: mime type of the item
        """
        GDItem.proper_paths(named_path, id_path)

        if named_path == '/':
            name = '/'
            gd_id = 'root'
            final_path = '/'
            final_id_path = ['root']
        else:
            split_path = named_path.split('/')
            name = split_path.pop()
            gd_id = id_path[-1]
            final_path = '/'.join(split_path)
            final_id_path = id_path[:-1]


        values = {
            'name': name,
            'id': gd_id,
            'mimeType': mime_type,
            'namedPath': final_path if final_path else '/',
            'idPath': final_id_path
        }
        super().__init__(values)

    @staticmethod
    def root():
        """ returns a GDItem corresponding to the root element """
        return GDItem('/', ['root'], gdconstants.FOLDER_MIME_TYPE)

    @staticmethod
    def folder(named_path, id_path):
        """ returns a GDItem as a folder """
        return GDItem(named_path, id_path, gdconstants.FOLDER_MIME_TYPE)

    @staticmethod
    def proper_paths(named_path, id_path):
        """ returns True when both paths are well defined:
            - absolute (start with root)
            - normalized (not containing relative stepss: ',' nor '..')
            - matching length
        """
        assert named_path.startswith('/'), "named path must be absolute"
        assert id_path[0] == 'root', "id_path must start with root"
        if named_path == '/':
            assert id_path == ['root'], "when named_path is /, id_path must be ['root']"
        else:
            split_path = named_path.split('/')
            print("XXX gditem.proper_paths() split_path", split_path)
            print("XXX                          id_path", id_path)
            assert len(split_path) == len(id_path), "named and id paths lengths must match"
            assert '.' not in split_path, "named path shouldn't contain a step '.'"
            assert '..' not in split_path, "named path shouldn't contain a step '..'"


    def is_folder(self):
        """ returns true if the item is a folder """
        return self['mimeType'] == gdconstants.FOLDER_MIME_TYPE

    def is_root(self):
        """ returns true if the item is root """
        return self['id'] == 'root'
