#! /usr/bin/env python3

"""
    Google Drive pwd

    This script shows the current working directory in the Google Drive
"""


import sys
import os

from gdconstants import _STATUS_FILENAME_EXPANDED
from gdconfig import GDConfig


def get_pwd():
    """ tryies to get current working directory from the status file.
        If the status file is not present, it creates one with default
        information.
        If the pwd is not present in the status file, it adds it and
        sets to the root directory
    """
    if not os.path.exists(_STATUS_FILENAME_EXPANDED):
        with open(_STATUS_FILENAME_EXPANDED, "w") as f:
            f.write('{}')
    status = GDConfig(_STATUS_FILENAME_EXPANDED)
    if not 'pwd' in status:
        status['pwd'] = 'root'
        status.store()
    return status['pwd']


def do_pwd(argv):
    """ shows the current working directory to the standard output
        @param argv: a list of str arguments (ignored in this version)
    """
    print(get_pwd())


def main():
    """ performs the interactive task of this module """
    do_pwd(sys.argv[1:])

if __name__ == '__main__':
    main()
