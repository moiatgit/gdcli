"""
    Google Drive item

    This module includes an encapsulation of an item in Google Drive

    It behaves as a dict but includes some specific aiding functions
"""

import os
import collections
import gdconstants

class GDItem(collections.UserDict):
    """ This class encapsulates a item in GD
        It behaves like a dict() with, at least, the following keys
        - name: item name
        - id:   item id at GD
        - mimeType: mime type as GD reported
        - named_path: list[str] with the absolute path (by default ['/'])
        - id_path: list of ids of folders to reach the item (first is always 'root')
    """

    def __init__(self, named_path, id_path, mime_type):
        """ initializes a new instance of a GD item
            @param named_path: list of str representing the steps of an absolute and
                               normalized path, as resulted from a call to
                               gdpath.normalize_splitted_path(gdpath.split_nixpath())
                   i.e. named_path must start with '/' and contain not '.' nor '..' steps.
            @param id_path: list of Google Drive ids composing the path to this item
            @param mime_type: mime type of the item
        """
        GDItem.proper_paths(named_path, id_path)

        if named_path == ['/']:
            name = '/'
            gd_id = 'root'
        else:
            name = named_path[-1]
            gd_id = id_path[-1]

        values = {
            'name': name,
            'id': gd_id,
            'mimeType': mime_type,
            'namedPath': named_path,
            'idPath': id_path
        }
        super().__init__(values)

    @staticmethod
    def root():
        """ returns a GDItem corresponding to the root element """
        return GDItem(['/'], ['root'], gdconstants.FOLDER_MIME_TYPE)

    @staticmethod
    def folder(named_path, id_path):
        """ returns a GDItem as a folder """
        return GDItem(named_path, id_path, gdconstants.FOLDER_MIME_TYPE)

    @staticmethod
    def proper_paths(named_path, id_path):
        """ returns True when both paths are well defined:
            - absolute (start with / and root respectively)
            - root just once (contain only / and root respectively)
            - normalized (not containing relative steps: '.' nor '..')
            - matching length
        """
        if not isinstance(named_path, list):
            raise TypeError(("named path must be a list[str]. "
                            "Found %s") % named_path)

        assert isinstance(id_path, list), "id path must be a list[str]"

        assert named_path[0] == '/', "named path must be absolute"
        assert named_path.count('/') == 1, ("named path must contain exactly one"
                                            "'/', %s found") % named_path.count('/')
        assert id_path.count('root') == 1, ("id path must contain exactly one"
                                            "'root', %s found") % id_path.count('/')
        assert id_path[0] == 'root', "id_path must start with root"
        if named_path == '/':
            assert id_path == ['root'], "when named_path is /, id_path must be ['root']"
        else:
            assert len(named_path) == len(id_path), ("named and id paths lengths must match, but\n"
                                                     "named path: %s (%s items)\n"
                                                     "id path   : %s (%s items)\n") % (
                                                         named_path,
                                                         len(named_path),
                                                         id_path,
                                                         len(id_path))
            assert '.' not in named_path, "named path shouldn't contain a step '.'"
            assert '..' not in named_path, "named path shouldn't contain a step '..'"


    def is_folder(self):
        """ returns true if the item is a folder """
        return self['mimeType'] == gdconstants.FOLDER_MIME_TYPE

    def is_root(self):
        """ returns true if the item is root """
        return self['id'] == 'root'

    def full_path(self):
        """ returns the full path to the item, including its name """
        return '/' + '/'.join(self['namedPath'][1:])

    def __hash__(self):
        """ the hash of a GDItem is the hash of its namedPath and name """
        return hash('/'.join(self['namedPath']))
