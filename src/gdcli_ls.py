#! /usr/bin/env python3

"""
    Google Driver cli: ls

    This script shows the files in the driver
"""

import sys
import os

import gdcore
import gdpath
import gdcli_pwd


def item_to_str(item):
    """ returns a printable representation of the GDItem """
    full_path = item.full_path()
    if item.is_folder():
        return os.path.join(full_path, '')
    return full_path


def print_items(folder, files):
    """ pretty prints the files """
    print("\nfolder: ", end='')
    if folder == '.':
        print(gdcli_pwd.get_pwd())
    else:
        print(folder)
    for item in files:
        print('\t%s' % item_to_str(item))
    print('total files: %s' % len(files))


def get_files(path):
    """ gets the files in the corresponding path.
        If path corresponds to a folder, it will return its contents.
        @param path: the path to the files to be listed
        @return: a list[GDItem] the list of items found matching requirements
        """
    found = []
    items = gdpath.items_from_path(path)
    for item in items:
        if item.is_folder():
            found += gdcore.get_items_by_folder(item)
        else:
            found.append(item)
    return found

def do_ls(argv):
    """ lists contents in Google Driver
        @param argv: a list of str arguments """
    if not argv:
        argv = ['.']
    print('Google Driver CLI: ls')
    for arg in argv:
        items = get_files(arg)
        print_items(arg, items)


def main():
    """ performs the interactive task of this module """
    do_ls(sys.argv[1:])

if __name__ == '__main__':
    main()
