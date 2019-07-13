"""
    Google Drive constants

    This is a bunch of constants for the gdcli suite

    It also includes some general use functions
"""
import os
import sys

_BASE_DIR = '~/.gdcli'
_GDCONFIG_FILENAME = 'gdconfig.json'
_DEFAULT_ENCODING = 'utf-8'
_STATUS_FILENAME = 'status.json'

_BASE_DIR_EXPANDED = os.path.expanduser(_BASE_DIR)
_DEFAULT_CONFIG_FILE_PATH = os.path.join(_BASE_DIR_EXPANDED, _GDCONFIG_FILENAME)
_STATUS_FILENAME_EXPANDED = os.path.join(_BASE_DIR_EXPANDED, _STATUS_FILENAME)

FOLDER_MIME_TYPE = 'application/vnd.google-apps.folder'

def print_error(msg):
    """ shows the message to stderr """
    print("\nERROR: " + msg + "\n", file=sys.stderr)


def print_error_and_exit(msg, error_code=1):
    """ shows the message to stderr and exits with given error code """
    print_error(msg)
    sys.exit(error_code)


def print_warning(msg):
    """ shows the message to the stderr as a warning """
    print("\nWARNING: " + msg + "\n", file=sys.stderr)


if __name__ == '__main__':
    print_error('This file is not intended to run alone')
    sys.exit(1)
