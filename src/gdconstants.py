"""
    Google Drive constants

    This is a bunch of constants for the gdcli suite
"""
import os

_BASE_DIR = '~/.gdcli'
_GDCONFIG_FILENAME = 'gdconfig.json'
_DEFAULT_ENCODING = 'utf-8'
_STATUS_FILENAME = 'status.json'

_BASE_DIR_EXPANDED = os.path.expanduser(_BASE_DIR)
_DEFAULT_CONFIG_FILE_PATH = os.path.join(_BASE_DIR_EXPANDED, _GDCONFIG_FILENAME)
_STATUS_FILENAME_EXPANDED = os.path.join(_BASE_DIR_EXPANDED, _STATUS_FILENAME)
