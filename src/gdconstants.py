"""
    Google Drive constants

    This is a bunch of constants for the gdcli suite
"""
import os

_BASE_DIR = '~/.gdcli'
_GDCONFIG_FILENAME = 'gdconfig.json'
_DEFAULT_ENCODING = 'utf-8'
_DEFAULT_CONFIG_FILE_PATH = os.path.expanduser(
        os.path.join(_BASE_DIR, _GDCONFIG_FILENAME))
