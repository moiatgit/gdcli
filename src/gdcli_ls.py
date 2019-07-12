#! /usr/bin/env python3

"""
    Google Driver cli: ls

    This script shows the files in the driver
"""

import sys
import json

import gdcore
import gdpath
import gdcli_pwd
from gdconstants import print_warning


_MIMETYPE_TO_EXTENSION_MAPPINGS = {
    'application/msword': 'msword',
    'application/pdf': 'pdf',
    'application/vnd.google-apps.document': 'document',
    'application/vnd.google-apps.folder': 'folder',
    'application/vnd.google-apps.form': 'form',
    'application/vnd.google-apps.spreadsheet': 'spreadsheet',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'gmldocument',
    'image/jpeg': 'jpeg',
}


def print_file(filespec):
    """ pretty prints the file spec """
    if 'fileExtension' in filespec:
        extension = ''
    else:
        extension = '{.%s}' % _MIMETYPE_TO_EXTENSION_MAPPINGS.get(filespec['mimeType'], 'unknown')
    size = '%s bytes' % filespec['size'] if 'size' in filespec else ''
    print('\t%s%s %s' % (filespec['name'], extension, size))


def print_files(folder, files):
    """ pretty prints the files """
    print("\nfolder: ", end='')
    if folder == '.':
        print(gdcli_pwd.get_pwd())
    else:
        print(folder)
    for item in files:
        print_file(item)
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
    for item in argv:
        files, error_msg = get_files(item)
        if error_msg:
            print_warning(error_msg)
            continue
        print_files(item, files)


def main():
    """ performs the interactive task of this module """
    do_ls(sys.argv[1:])

if __name__ == '__main__':
    main()
