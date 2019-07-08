"""
    Google Drive path

    This module encapsulates translation from user friendly paths to Google Drive paths
"""
from gdstatus import get_status

def path_to_gd(path='.'):
    """ translates path to a Google Drive item.
        It returns a tuple with values:
            id: the corresponding id, or empty when error
            error_msg: a description of the error, empty when no error
    """
    path_id = error_msg = ''

    # normalize: absolute and relative paths
    path_items = path.split('/')
    if path.startswith('/'):
        gd_ids = ['root']
        print("XXX added root")
    else:
        gd_ids = get_status()['pwd_id']

    while path_items:
        item = path_items.pop(0)
        item_info = get_file(gd_ids[-1])
        print('XXX item_info', item_info)

    if not error_msg:
        print("XXX gd_ids", gd_ids)
        path_id = gd_ids[-1]
        print("XXX\t path_id", path_id)

    return (path_id, error_msg)
