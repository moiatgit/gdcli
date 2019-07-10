"""
    Google Drive path

    This module encapsulates translation from user friendly paths to Google Drive paths
"""
import collections
import gdstatus
import gdcli_pwd
import gdcore
import gdconstants

class GDItem(collections.UserDict):
    """ This class encapsulates a item in GD
        It behaves like a dict() with, at least, the following keys
        - name: item name
        - id:   item id at GD
        - mimeType: mime type as GD reported
        - named_path: list of name of folders to reach the item (first is always root '/')
        - id_path: list of ids of folders to reach the item (first is always 'root')
    """

    def __init__(self, name, gd_id, mime_type, named_path=['/'], id_path=['root']):
        """ initializes a new instance of a GD item
            @param name: name of the item
            @param gd_id: GD id
            @param mime_type: mime type of the item
            @param named_path: list of names composing the path to this item
            @param id_path: list of ids composing the path to this item
        """
        d = {
            'name': name,
            'id': gd_id,
            'mimeType': mime_type,
            'namedPath': named_path,
            'idPath': id_path,
        }
        super().__init__(d)

    def is_folder(self):
        """ returns true if the item is a folder """
        return filespec['mimeType'] == gdconstants._FOLDER_MIME_TYPE

    def is_root(self):
        """ returns true if the item is root """
        return self['id'] == 'root'





def path_to_gd(path='.'):
    """ translates path to a GDItem
        It returns a tuple with values:
            item: the corresponding item, or empty when error
            error_msg: a description of the error, empty when no error
    """
    print("XXX gdpath.path_to_gd(path: %s)" % path)
    gd_id = error_msg = ''

    if path == '/':
        name = '/'
        gd_id = 'root'
        mime_type = gdconstants._FOLDER_MIME_TYPE
    else:
        # normalize: absolute and relative paths
        path_items = [ item for item in path.split('/') if item.strip() ]
        print("XXX\tpath_items:", path_items)
        if path.startswith('/'):
            gd_ids = ['root']
        else:
            gd_ids = gdstatus.get_status()['pwd_id']
        print("XXX\tgd_ids:", gd_ids)

        while path_items:
            item = path_items.pop(0)
            print("XXX\t>>> considering item %s with rest path_items %s" % (item, path_items))
            if item == '.':
                continue
            if item == '..':
                if len(gd_ids) > 1:
                    gd_ids.pop()
                continue

            gd_items = gdcore.get_file(item, folder=gd_ids[-1])
            print("XXX\t>>> gdcore.get_file() returns", gd_items)

            if not gd_items:    # item not found
                error_msg = "element not found: %s" % item
                break

            if path_items:  # item must be a folder
                gd_items = [ gd_item for gd_item in gd_items if gdcore.is_folder(gd_item) ]
                if not gd_items: # none of the items found was a folder
                    error_msg = "not a directory: %s" % item
                    break

            if len(gd_items) > 1:
                gdconstants.print_warning('more than one item named as %s' % item)
            item_info = gd_items[0]
            gd_ids.append(item_info['id'])
            print("XXX\t>>> item %s results in %s with gd_ids %s" % (item, item_info['id'], gd_ids))

        if not error_msg:
            gd_id = gd_ids[-1]

    return (GDItem(name, gd_id, mime_type),  error_msg)


