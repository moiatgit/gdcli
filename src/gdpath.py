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
    path_items = normalize_splitted_path(split_nixpath(path))

    # trivial cases
    if path_items == ['/']:
        return [gditem.GDItem.root()]

    if path_items == ['']:
        return [gdcli_pwd.get_pwd_gditem()]

    # absolute or relative
    if path_items.startswith('/'):
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

    # get rid of '..'
    result = []
    while path:
        step = path.pop(0)
        if step == '..' and result and result[-1] != '..':
            result.pop()
        else:
            result.append(step)
    return result


