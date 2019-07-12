"""
    Google Drive path

    This module encapsulates translation from user friendly paths to Google Drive paths
"""

import os.path
import collections

import gdcli_pwd
import gditem
import gdcli_pwd
import gdcore
import gdconstants

class GDPath(collections.UserDict):
    """ encapsulates a path
        It behaves like a dict() with the following keys
        - 'nixPath': a str containing the *nix like path as given on __init__
        - 'translationOK': a boolean that indicates whether the translation of
                           nixPath was successful or not

        Depending on the value of 'translationOK', one of the following keys will be present
        - 'items': a list of gditems matching the nixPath in Google Drive
        - 'errorMessage': an error message in case not translationOK.

        Google Drive filesystem presents the peculiarity that items' names are not unique in
        a given folder. This implies that a *nix-like path can represent more than one file.

        The errors that can arise from translation are:

        - a step in the path is not found': Google Drive has no item matching the path
        - a step in the path is not a directory: a certain step in the path corresponds to one or
                             more items in GD but none of them are folders
    """
    def __init__(self, path):
        """ constructs a GDPath from the *nix-like path
            @param path: str describing a *nix like path
        """
        values = {
            'nixPath': path,
            'translationOK': True,
        }
        super().__init__(values)
        self._translate_path()


    @staticmethod
    def _process_path_items(path_items, partial_id_path, final_path):
        """ given a list of items to process, and the partial id_path
            it explores whether it is possible to complete the path items.

            @return list[GDItem]: the list of items found in GD if no error found
                    error_message: the error message if an error was found
        """
        found = []
        error_msg = ''
        mime_type = gdconstants.FOLDER_MIME_TYPE
        while path_items:
            current = path_items.pop(0)

            # get files with current item name
            gd_items = gdcore.get_file(current, folder=id_path[-1])
            if not gd_items:
                error_msg += "not found: %s" % current
                break

            for gdi in gd_items:
                if path_items:
                    if not gdi.is_folder():
                        error_msg += "not a directory: %s" % current
                        continue
                    found += _process_path_items(path_items, 

                                                 PROBLEM: deciding whether current doesn't produce any result because it is missing in GD or it is not a directory
                                                 is producing a lot of difficulty.
                                                 Proposal: consider only the case of error "no found"
                                                 You know it just because _process_path_items() results in an empty list
                id_path = partial_id_path[:] + gdi['id']
                mime_type = gd_item['mimeType']


    def _translate_path(self):
        """ It translates self['nixPath'] to a list[GDItem], and
            sets keys 'translationOK', 'items' and 'errorMessage'
            accordingly
        """
        path = os.path.normpath(path)

        # trivial cases
        if path == '/':
            self['items'] = [gditem.GDItem.root()]
            return

        if path == '.':
            self['items'] = [gdcli_pwd.get_pwd_gditem()]
            return

        # non trivial cases
        path_items = path.split('/')
        if path.startswith('/'):
            id_path = ['root']
            path_items.pop(0)   # get rid of root
        else:
            id_path = gdcli_pwd.get_pwd_id_path()

        pwd = gdcli_pwd.get_pwd()

        # remove back to parent steps ../
        while pwd and path_items and path_items[0] == '..':
            path_items.pop(0)
            pwd = os.path.dirname(pwd)
            if len(id_path) > 1:    # do not touch root
                id_path.pop()
        path = '/'.join(path_items)

        # correct final path from pwd
        if not path.startswith('/'):
            final_path = os.path.join(pwd, path) if path else pwd
        else:
            final_path = path

        # initial item is sure a folder
        mime_type = gdconstants.FOLDER_MIME_TYPE

        paths_found = _process_path_items(path_items, id_path)

    #return gditem.GDItem(final_path, id_path, mime_type), ""




def named_path_to_gd_item(path=''):
    """ translates path to a GDItem
        It returns a tuple with:
        - item: a GDItem corresponding to the given path. None when error
        - error_msg: a str describing the problem found when trying translation.
                     Empty str when no error.

        @param path: str specifying a *nix-like path
    """
    path = os.path.normpath(path)


    if path == '/':
        return gditem.GDItem.root(), ""

    if path == '.':
        return gdcli_pwd.get_pwd_gditem(), ""

    path_items = path.split('/')
    if path.startswith('/'):
        id_path = ['root']
        path_items.pop(0)   # get rid of root
    else:
        id_path = gdcli_pwd.get_pwd_id_path()

    pwd = gdcli_pwd.get_pwd()

    # remove back to parent steps ../
    while pwd and path_items and path_items[0] == '..':
        path_items.pop(0)
        pwd = os.path.dirname(pwd)
        if len(id_path) > 1:    # do not touch root
            id_path.pop()
    path = '/'.join(path_items)

    # initial item is sure a folder
    mime_type = gdconstants.FOLDER_MIME_TYPE
    while path_items:
        current = path_items.pop(0)

        # get files with current item name
        gd_items = gdcore.get_file(current, folder=id_path[-1])
        if not gd_items:
            return None, "not found: %s" % current

        # remember: it can be more than one item equally named on the same path
        # any of them will do for the purposes of this method
        gd_item = gd_items[0]
        if path_items and not gd_item.is_folder():
            return None, "not a directory: %s" % current
        id_path.append(gd_item['id'])
        mime_type = gd_item['mimeType']

    if not path.startswith('/'):
        final_path = os.path.join(pwd, path) if path else pwd
    else:
        final_path = path

    return gditem.GDItem(final_path, id_path, mime_type), ""



