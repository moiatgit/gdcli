"""
    Google Drive path

    This module encapsulates translation from user friendly paths to Google Drive paths
"""

import os.path
import gdcli_pwd
import gditem
import gdcli_pwd
import gdcore
import gdconstants

def normalize_path(path):
    """ normalizes the path so:
        - it becomes absolute
        - it does not contain '.' nor '..' steps """
    if not path.startswith('/'):
        pwd = gdcli_pwd.get_pwd()
        path = os.path.join(pwd, path)
    return os.path.normpath(path)


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
    print("XXX UUU once removed .. pwd=%s id_path=%s path_items=%s" % (pwd, id_path, path_items))
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
        print("XXX joining from pwd %s and path %s" % (pwd, path))
    else:
        final_path = path
    print("XXX final_path   ", final_path)
    print("XXX final id_path", id_path)

    return gditem.GDItem(final_path, id_path, mime_type), ""



