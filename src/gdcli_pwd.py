#! /usr/bin/env python3

"""
    Google Drive pwd

    This script shows the current working directory in the Google Drive
"""


import sys



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
