"""
    Google Drive path

    This module encapsulates translation from user friendly paths to Google Drive paths
"""
from gdstatus import get_status
from gdcore import get_file

def path_to_gd(path='.'):
    """ translates path to a Google Drive item.
        It returns a tuple with values:
            id: the corresponding id, or empty when error
            error_msg: a description of the error, empty when no error
    """
    path_id = error_msg = ''

    # normalize: absolute and relative paths
    print("XXX path before anything '%s'" % path)
    path_items = [ item for item in path.split('/') if item.strip() ]
    if path.startswith('/'):
        gd_ids = ['root']
        print("XXX added root")
    else:
        gd_ids = get_status()['pwd_id']

    print("XXX path_items before while", path_items)
    while path_items:
        item = path_items.pop(0)
        print("XXX in the while checking item", item)
        items = get_file(gd_ids[-1])
        print("XXX items from get_file(%s): %s" %(gd_ids[-1], items))
        if not items:
            error_msg = "element not found: %s" % item
            break
        print('XXX item_info', item_info)

    if not error_msg:
        print("XXX get path_id from last ", gd_ids[-1])
        path_id = gd_ids[-1]
    print("XXX once processed path_items")
    print("\terror_msg '%s'" % error_msg)
    print("\tgd_ids %s" % gd_ids)
    print("\tpath_id '%s'" % path_id)

    return (path_id, error_msg)
