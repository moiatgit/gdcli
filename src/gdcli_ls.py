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
        If path is a file, it will return just one file if exists.
        @param path: the path to the files to be listed
        @return: a tuple:
            items found: the list of items found matching requirements if no error
            error message: the error message if any
        """
    item_id, error_msg = gdpath.path_to_gd(path)
    if error_msg:
        return ([], error_msg)
    if gdcore.is_folder(item_id):
        XXX the problem is that gdpath.path_to_gd() is not returning if the item is a folder or not
        once known, it should call gdcore.get_list() only when item_id is sure to belong to a folder
    files = gdcore.get_list(item_id)
    if files:
        return (files, '')
    error_msg = 'No files found for %s' % path
    return ([], error_msg)


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
