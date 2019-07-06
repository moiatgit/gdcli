"""
    Google Drive configuration

    This module is an utility to configure Google Drive utilities

    It behaves just like a dict initialized with the contents of _DEFAULT_CONFIG_FILE_PATH

    Note: any key ended by '_path' will be user expanded with os.path.expanduser()
"""
import os
import collections
import json
import logging


class GDConfig(collections.UserDict):
    """ This class behaves like a dict() except it is preloaded with configuration
        data.
    """

    _DEFAULT_CONFIG_FILE_PATH = os.path.expanduser('~/.gdcli/gdconfig.json')
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
        try:
            d = json.loads(contents, encoding=encoding)
        except json.decoder.JSONDecodeError as e:
            logging.error('Problems trying to decode file %s as json: %s' % (
                config_path,
                e))
            d = {}

        super().__init__(d)

        # expand paths
        for key in self:
            if key.endswith('_path'):
                self[key] = os.path.expanduser(self[key])
                if not self[key].startswith('/'):
                    self[key] = os.path.join(os.path.dirname(config_path), self[key])

    def check_ok(self):
        """ returns true when the contents are the expected ones """
        return all((k in self) for k in ('client_secrets_path', 'token_path', 'scopes'))
