#! /usr/bin/env python3

"""
    Google Driver cli: ls

    This script shows the files in the driver
"""

import sys
import json

from gdcore import get_list
from gdcli_pwd import get_pwd


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
        extension = '.{%s}' % _MIMETYPE_TO_EXTENSION_MAPPINGS.get(filespec['mimeType'], 'unknown')
    size = '%s bytes' % filespec['size'] if 'size' in filespec else ''
    print('%s%s %s' % (filespec['name'], extension, size))

def print_files(files):
    """ pretty prints the files """
    print('Google Driver CLI: ls')
    for item in files['files']:
        print_file(item)
    print('\ntotal files: %s' % len(files['files']))

def do_ls(argv):
    """ lists contents in Google Driver
        @param argv: a list of str arguments """
    if argv:
        print_warning("ls not implemented yet with arguments")
    files = get_list(get_pwd())
    print(json.dumps(files))
    print("XXXXXX")
    print_files(files)

def main():
    """ performs the interactive task of this module """
    do_ls(sys.argv[1:])

if __name__ == '__main__':
    main()
