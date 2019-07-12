#! /usr/bin/env python3

"""
    Google Drive CLI: pwd

    This script shows the current working directory in the Google Drive
"""


import sys

import gdstatus
import gditem

def get_pwd():
    """ returns the current working directory """
    return gdstatus.get_status()['pwd']

def get_pwd_id():
    """ returns the current working directory id """
    return gdstatus.get_status()['pwd_id'][-1]

def get_pwd_id_path():
    """ returns the current working directory path as a list of id"""
    return gdstatus.get_status()['pwd_id']

def get_pwd_gditem():
    """ returns the current working directory as a GDItem """
    status = gdstatus.get_status()
    return gditem.GDItem.folder(status['pwd'], status['pwd_id'])

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
