"""
    Google Drive path

    This module encapsulates translation from user friendly paths to Google Drive paths
"""

import os.path

import gdcli_pwd
import gditem
import gdcore


def _process_path_items(former_path_items, partial_id_path, partial_named_path, final_path):
    """ given a list of items to process, and the partial id_path
        it tries to complete path_items to construct matching GDItem

        @return list[GDItem]: the list of items found in GD matching the final
                              path
    """
    found = []
    path_items = former_path_items[:]
    current = path_items.pop(0)
    print("XXXgdpath._process_path_items path_items", path_items)
    folder = gditem.GDItem.folder(partial_named_path, partial_id_path)
    gd_items = gdcore.get_items_by_name(current, folder=folder)
    for gdi in gd_items:
        id_path = partial_id_path[:] + [gdi['id']]
        if path_items:
            if not gdi.is_folder():
                continue
            named_path = os.path.join(partial_named_path, gdi.full_path())
            found += _process_path_items(path_items, id_path, named_path, final_path)
        else:
            mime_type = gdi['mimeType']
            new_item = gditem.GDItem(final_path, id_path, mime_type)
            found.append(new_item)
    return found


def items_from_path(path):
    """ It translates self['nixPath'] to a list[GDItem], and
        sets keys 'translationOK', 'items' and 'errorMessage'
        accordingly
    """
    print("XXX gdpath.items_from_path(path: %s)" % path)
    path = os.path.normpath(path)

    # trivial cases
    if path == '/':
        return [gditem.GDItem.root()]

    if path == '.':
        return [gdcli_pwd.get_pwd_gditem()]

    # absolute or relative
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

    # trivial case: it was a list of ../
    if not path_items:
        return [gditem.GDItem.folder(final_path, id_path)]

    return _process_path_items(path_items, id_path, pwd, final_path)
