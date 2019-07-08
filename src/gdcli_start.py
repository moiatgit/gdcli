#! /usr/bin/env python3

"""
    Google Drive start

    This module is an utility to start Google Drive utilities

    The rest of the suite could not work properly if this script doesn't end with an OK status
"""

import os
import os.path
import sys

from gdconstants import _BASE_DIR, _GDCONFIG_FILENAME, print_error_and_exit
import gdconfig
from gdcore import get_driver

_EXPECTED_CONTENTS_IN_GDCONFIG = (
    '\t{\n'
    '\t  "client_secrets_path": "client_secrets.json",\n'
    '\t  "token_path": "token.json",\n'
    '\t  "scopes": "https://www.googleapis.com/auth/drive"\n'
    '\t}\n\n'
    'Notes: These values can be changed if you know what you are doing.\n'
    '       Keys suffixed with _path admit a relative path (e.g. ~/anyfolder/filename)\n')

def do_start(argv):
    """ checks that everything is ok to run the app.
        @param argv: a list of str arguments (ignored in this version)
    """

    print('Google Drive CLI: initial configuration utility\n')

    # base dir is present and accessible
    base_dir = os.path.expanduser(_BASE_DIR)
    if not os.path.exists(base_dir):
        print_error_and_exit(('Missing folder {0}\n'
                              'Tip: create the folder {0}\n'
                              '\t$ mkdir {0}').format(_BASE_DIR))

    if not os.path.isdir(base_dir):
        print_error_and_exit(('Entry {0} is not a folder\n'
                              'Tip: rename this file first\n'
                              '\t  $ mv -vi {0} {0}.bak\n').format(_BASE_DIR))

    if not os.access(base_dir, os.R_OK|os.W_OK):
        print_error_and_exit(('Folder {0} has wrong permissions\n'
                              'Tip: allow read and write access to this folder\n'
                              '\t$ chmod u+rwx {0}\n').format(_BASE_DIR))

    # config filename is present
    gdconfig_path = os.path.join(base_dir, _GDCONFIG_FILENAME)
    gdconfig_path_unexpanded = os.path.join(_BASE_DIR, _GDCONFIG_FILENAME)
    if not os.path.exists(gdconfig_path):
        print_error_and_exit(('Missing proper configuration file %s\n'
                              'Tip: open a text file named %s with your favorite editor '
                              'and place inside the following contents:\n\n%s'
                              ) % (gdconfig_path_unexpanded,
                                   gdconfig_path_unexpanded,
                                   _EXPECTED_CONTENTS_IN_GDCONFIG))

    # config filename contains expected keys
    config = gdconfig.GDConfig(gdconfig_path)
    for key in ('client_secrets_path', 'token_path', 'scopes'):
        if key not in config:
            print_error_and_exit(('Missing key {0} in file {1}\n'
                                  'Tip: open the file {1} with your favorite editor '
                                  'and place inside the following contents:\n\n'
                                  '{2}\n'.format(key, gdconfig_path_unexpanded,
                                                 _EXPECTED_CONTENTS_IN_GDCONFIG)))

    # the expected secrets are where they should
    if not os.path.exists(config['client_secrets_path']):
        print_error_and_exit(('Missing file {0}\n'
                              'Tip: gdcli requires this file to authenticate '
                              'with Google Drive using OAuth 2.0\n'
                              'Visit the following url to get instructions on how to '
                              'obtain file {0}\n'
                              '\thttps://developers.google.com/identity/protocols/OAuth2\n'
                              'Note: when you are asked for permissions, remember the '
                              'ones you defined in the scopes key:\n\t{1}').format(
                                  config['client_secrets_path'],
                                  config['scopes']))

    # the token is already downloaded
    get_driver()

    # everything went OK
    print(('Congratulations. Your Google Drive CLI is ready for use\n'
           'Tip: to continue consider getting some help\n'
           '$ gdcli help\n'))

def main():
    """ performs the interactive task of this module """
    do_start(sys.argv[1:])

if __name__ == '__main__':
    main()
