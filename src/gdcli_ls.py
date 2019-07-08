#! /usr/bin/env python3

"""
    google drive cli: ls

    This script shows the files in the driver
"""

import sys
import json

from gdcore import get_driver
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

def get_list(drive, folder='root'):
    """ returns the list of files in the folder """
    fields = 'files(id,name,mimeType,size,fileExtension)'
    return drive.files().list(
        q="'%s' in parents and trashed=false" % folder,
        fields=fields
    ).execute()

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
    print('Google Drive CLI: ls')
    for item in files['files']:
        print_file(item)
    print('\ntotal files: %s' % len(files['files']))

def do_ls(argv):
    """ lists contents in Google Drive
        @param argv: a list of str arguments (ignored in this version) """
    driver = get_driver()
    files = get_list(driver, get_pwd())
    print(json.dumps(files))
    print("XXXXXX")
    print_files(files)

def main():
    """ performs the interactive task of this module """
    do_ls(sys.argv[1:])

if __name__ == '__main__':
    main()
