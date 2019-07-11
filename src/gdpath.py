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
    path = normalize_path(path)

    if path == '/':
        return gditem.GDItem.root(), ""

    path_items = path.split('/')[1:]
    print("XXX path_items (initial)", path_items)
    id_path = ['root']
    mime_type = gdconstants.FOLDER_MIME_TYPE
    while path_items:
        print("XXX checking path_items", path_items)
        current = path_items.pop(0)
        print("XXX\tcurrent: ", current)
        gd_item = gdcore.get_file(current, folder=id_path[-1])
        if not gd_item:
            return None, "not found: %s" % current
        if path_items and not gd_item.is_folder():
            return None, "not a directory: %s" % current
        id_path.append(gd_item['id'])
        mime_type = gd_item['mimeType']
    print("XXX finally path    ", os.path.dirname(path))
    print("XXX         id_path ", id_path)

    return gditem.GDItem(os.path.dirname(path), id_path, mime_type), ""



def path_to_gd(path=''):
    """ translates path to a GDItem
        It returns a tuple with values:
            item: the corresponding item, or None when error
            error_msg: a description of the error, empty when no error
    """
    print("XXX gdpath.path_to_gd(path: %s)" % path)

    if path == '/':
        pass

    gditems = []    # list of GDItem. Lower is root

    # normalize: absolute and relative paths
    path_items = [ item for item in path.split('/') if item.strip() ]
    name = path_items.pop()
    if path.startswith('/'):
        id_path = ['root']
        named_path = '/'
        print("XXX\tname_path when absolute", named_path)
    else:
        id_path = gdstatus.get_status()['pwd_id']
        named_path = gdstatus.get_status()['pwd']
        print("XXX\tname_path when relative", named_path)
    print("XXX\tpath_items:", path_items)
    print("XXX\tname_path: ", named_path)
    print("XXX\tid_path:", id_path)

    while path_items:
        item_name = path_items.pop(0)
        print("XXX\t>>> considering item %s with rest path_items %s" % (item_name, path_items))

        if item_name == '.':    # ignore references to current folder
            continue

        if item_name == '..':   # back one step in the path
            if len(id_path) > 1:
                id_path.pop()
            continue

        gd_items = gdcore.get_file(item, folder=id_path[-1])
        print("XXX\t>>> gdcore.get_file() returns", gd_items)

        if not gd_items:    # item not found
            return None, "element not found: %s" % item

        if path_items:  # item must be a folder
            gd_items = [ gd_item for gd_item in gd_items if gdcore.is_folder(gd_item) ]
            if not gd_items: # none of the items found was a folder
                error_msg = "not a directory: %s" % item
                break

        if len(gd_items) > 1:
            gdconstants.print_warning('more than one item named as %s' % item)
        item_info = gd_items[0]
        id_path.append(item_info['id'])
        mime_type = item_info['mimeType']
        print("XXX\t>>> item %s results in %s with id_path %s" % (item, item_info['id'], id_path))

    if error_msg:
        item = None
    else:
        gd_id = id_path.pop()
        item = gditem.GDItem(name, gd_id, mime_type, named_path, id_path)

    return (item,  error_msg)


