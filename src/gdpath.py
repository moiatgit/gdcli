"""
    Google Drive path

    This module encapsulates translation from user friendly paths to Google Drive paths
"""

import os.path

import gdcli_pwd
import gditem
import gdcore


def _process_path_items(former_remaining_path_items, partial_id_path, partial_named_path, final_path):
    """ given a list of items to process, and the partial id_path
        it tries to complete remaining_path_items to construct matching GDItem

        @return list[GDItem]: the list of items found in GD matching the final
                              path
    """
    print("XXX _process_path_items()")
    print("XXX\t former_remaining_path_items", former_remaining_path_items)
    print("XXX\t partial_id_path", partial_id_path)
    print("XXX\t partial_named_path", partial_named_path)
    print("XXX\t final_path", final_path)
    found = []
    remaining_path_items = former_remaining_path_items[:]
    current = remaining_path_items.pop(0)
    folder = gditem.GDItem.folder(partial_named_path, partial_id_path)
    print("XXX attempting to call API")
    print("XXX\t current", current)
    print("XXX\t folder", folder)
    gd_items = gdcore.get_items_by_name(current, folder=folder)
    for gdi in gd_items:
        print("XXX\t\t considering gdi", gdi)
        id_path = gdi['idPath']
        named_path = gdi['namedPath']
        if remaining_path_items:
            if not gdi.is_folder():
                continue
            found += _process_path_items(remaining_path_items, id_path, named_path, final_path)
        else:
            mime_type = gdi['mimeType']
            new_item = gditem.GDItem(named_path, id_path, mime_type)
            found.append(new_item)
    return found


def items_from_path(path):
    """ It translates self['nixPath'] to a list[GDItem], and
        sets keys 'translationOK', 'items' and 'errorMessage'
        accordingly
    """
    print("XXX items_from_path(path: %s)" % path)
    # trivial case: root
    if path == '/':
        return [gditem.GDItem.root()]

    remaining_items = normalize_splitted_path(split_nixpath(path))

    # trivial case: pwd
    if remaining_items == ['']:
        return [gdcli_pwd.get_pwd_gditem()]

    # absolute or relative
    if path.startswith('/'):
        id_path = ['root']
        pwd = ['/']
        remaining_items.pop(0)   # get rid of root
    else:
        id_path = gdcli_pwd.get_pwd_id_path()
        pwd = gdcli_pwd.get_pwd_splitted()

    print("XXX\t remaining_items", remaining_items)
    print("XXX\t id_path", id_path)
    print("XXX\t pwd", pwd)

    # remove back to parent steps ../
    while pwd and remaining_items and remaining_items[0] == '..':
        remaining_items.pop(0)
        if len(id_path) > 1:    # do not touch root
            id_path.pop()
            pwd.pop()
    path = '/'.join(remaining_items)

    if remaining_items:
        final_path = pwd + remaining_items
        return _process_path_items(remaining_items, id_path, pwd, final_path)
    else:
        return [gditem.GDItem.folder(pwd, id_path)]


def split_nixpath(nixpath):
    """ given a *nix-like path, it returns the list of steps.
        It works similar to nixpath.split('/') but it:
        - takes into account escaped slashes,
        - keeps initial slash as a result

        Basically, GD names allow virtually any character including slashes.
        Slashes make nix-like paths go crazy
        The adopted solution has been to allow escaping with backslash.
        Therefore, '\/' will be translated as '/'
                   double \ will go as single
    """
    # trivial path
    if not nixpath:
        return ['']

    result = []

    # absolute paths
    if nixpath.startswith('/'):
        nixpath = nixpath[1:]
        result.append('/')

    # rest of path
    current_name = ''
    while nixpath:
        current_chr = nixpath[0]
        nixpath = nixpath[1:]
        if current_chr == '\\':     # it can't be the last one or OS would have complained
            current_name += nixpath[0]
            nixpath = nixpath[1:]
        elif current_chr == '/':    # considered as a path delimiter
            result.append(current_name)
            current_name = ''
        else:
            current_name += current_chr
    if current_name:
        result.append(current_name)
    return result


def normalize_splitted_path(splitted_path):
    """ given a list of steps forming a path (as result of split_nixpath() for
        example), it
        returns the path normalized so:
        - steps '.' are ignored
        - steps '..' remove previous non-'..' steps
    """
    # get rid of '.'
    path = [ step for step in splitted_path if step != '.']
    if not path:
        return ['']

    # get rid of '..'
    result = []
    while path:
        step = path.pop(0)
        if step == '..':
            if result:
                if result[-1] == '/':
                    pass        # do not remove root
                elif result[-1] == '..':
                    result.append(step)
                else:
                    result.pop()
            else:
                result.append(step)
        else:
            result.append(step)
    return result


