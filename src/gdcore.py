"""
    Google drive core

    This file contains core features for the Google drive utilities
"""

import os
from oauth2client import file, client, tools
from googleapiclient.discovery import build

import gdconstants
import gdconfig
import gditem

# a sort of singleton containing the Google Drive driver once authenticated
_driver = None

def authenticate(token, client_secrets, scopes):
    """ performs the authentication and returns the service,
        Params:
            token: is the path of the file where the token should be stored
            client_secrets: is the path to the file containing the credentials
            scopes: is the list of scopes required to perform the actions
    """
    store = file.Storage(token)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(client_secrets, scopes)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', credentials=creds, cache_discovery=False)
    return service


def get_driver():
    """ returns a driver connected to the service
        It has into account the settings in GDConfig """
    if not _driver:
        config = gdconfig.GDConfig()
        _driver = authenticate(
            config['token_path'],
            config['client_secrets_path'],
            config['scopes'])
    return _driver


def _gdcontents_to_gditem(contents, gdfolder):
    """ given a response of a Google Drive query, it return the list
        of GDItems contained in the 'files' entry if present
        @param contents: a dict as return by a query to Google Driver
    """
    return [gditem.GDItem(os.path.join(gdfolder['namedPath'], item['name']),
                          gdfolder['idPath'] + [item['id']],
                          item['mimeType']) for item in contents.get('files', [])]


def get_items_by_name(name, gdfolder):
    """ it returns the contents from gdfolder with the given name.
        Note: Google Drive allows multiple files equally named in the same folder!

        @param name: str defining the name of the item to find
        @param gdfolder: a GDItem such that gdfolder.is_folder() == True
        @return list[GDItem]
    """
    fields = 'files(id,name,mimeType)'
    parent = gdfolder['id']
    result = get_driver().files().list(
        q="name='%s' and '%s' in parents and trashed=false" % (name, parent),
        spaces='drive',
        fields=fields
    ).execute()
    return _gdcontents_to_gditem(result, gdfolder)

def get_items_by_folder(gdfolder):
    """ it returns the contents from gdfolder
        @param gdfolder: a GDItem such that gdfolder.is_folder() == True
        @return list[GDItem]
    """
    fields = 'files(id,name,mimeType)'
    parent = gdfolder['id']
    result = get_driver().files().list(
        q="'%s' in parents and trashed=false" % parent,
        spaces='drive',
        fields=fields
    ).execute()
    return _gdcontents_to_gditem(result, gdfolder)

if __name__ == "__main__":
    gdconstants.print_error_and_exit('This file is not intended to run alone')
