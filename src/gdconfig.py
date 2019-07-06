"""
    Google Drive configuration

    This module is an utility to configure Google Drive utilities

    It behaves just like a dict initialized with the contents of _DEFAULT_CONFIG_FILE_PATH

    Note: any key ended by '_path' will be user expanded with os.path.expanduser()
"""
import os
import collections
import json


class GDConfig(collections.UserDict):
    """ This class behaves like a dict() except it is preloaded with configuration
        data.
    """

    _DEFAULT_CONFIG_FILE_PATH = 'gdconfig.json'
    _DEFAULT_ENCODING = 'utf-8'

    def __init__(self,
                 config_path=_DEFAULT_CONFIG_FILE_PATH,
                 encoding=_DEFAULT_ENCODING):
        """ initializes a new instance:
            @param config_path: str with the path to the file with the configuration data
            @param encoding: str with the name of the encoding in the configuration data
        """
        with open(config_path, encoding='utf8') as f:
            contents = f.read()
        super().__init__(json.loads(contents, encoding=encoding))
        for key in self:
            if key.endswith('_path'):
                self[key] = os.path.expanduser(self[key])
