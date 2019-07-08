"""
    Google Drive path

    This module encapsulates translation from user friendly paths to Google Drive paths
"""
import gdstatus
import gdcli_pwd
import gdcore

def path_to_gd(path='.'):
    """ translates path to a Google Drive item.
        It returns a tuple with values:
            id: the corresponding id, or empty when error
            error_msg: a description of the error, empty when no error
    """
    print("XXX path_to_gd(path:'%s') enters" % path)
    path_id = error_msg = ''

    # normalize: absolute and relative paths
    path_items = [ item for item in path.split('/') if item.strip() ]
    if path.startswith('/'):
        gd_ids = ['root']
    else:
        gd_ids = gdstatus.get_status()['pwd_id']
    print("XXX\tpath_items", path_items)
    print("XXX\tgd_ids", gd_ids)

    while path_items:
        print("XXX\t\tin the while, path_items", path_items)
        item = path_items.pop(0)
        if item == '.':
            print("XXX\t\tignoring . gd_ids:", gd_ids)
            continue
        if item == '..':
            raise 'not supported parent ref yet'
        gd_items = gdcore.get_file(item, folder=gd_ids[-1])
        if not gd_items:
            error_msg = "element not found: %s" % item
            break
        if len(gd_items) > 1:
            print_warning('More than one item named as %s' % item)
        item_info = gd_items[0]
        gd_ids.append(item_info['id'])
        print('XXX item_info', item_info)
        print('XXX now gd_ids', gd_ids)

    print("XXX\tfinished while. gd_ids", gd_ids)
    if not error_msg:
        path_id = gd_ids[-1]
    print("\terror_msg '%s'" % error_msg)
    print("\tgd_ids %s" % gd_ids)
    print("\tpath_id '%s'" % path_id)

    return (path_id, error_msg)


