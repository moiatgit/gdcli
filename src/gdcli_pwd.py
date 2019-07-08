#! /usr/bin/env python3

"""
    Google Drive CLI: pwd

    This script shows the current working directory in the Google Drive
"""


import sys

import gdstatus

def get_pwd():
    """ returns the current working directory """
    pwd_path = gdstatus.get_status()['pwd']
    return "/".join(pwd_path) if len(pwd_path) > 1 else '/'

def get_pwd_id():
    """ returns the current working directory id """
    return gdstatus.get_status()['pwd_id'][-1]

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
