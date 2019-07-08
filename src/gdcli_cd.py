#! /usr/bin/env python3

"""
    Google Drive cli: cd

    This script allows changing current directory in the driver
"""

import sys

from gdconstants import print_warning
from gdstatus import get_status

def do_cd(argv):
    """ changes the current directory to a given one
    @param argv: a list of str arguments. It expects one: the new directory
    If no argument s given, it defaults to root
    """

    status = get_status()
    if argv:
        print_warning("not implemented yet")
    else:
        status['pwd'] = 'root'

def main():
    """ performs the interactive task of this module """
    do_cd(sys.argv[1:])

if __name__ == '__main__':
    main()
