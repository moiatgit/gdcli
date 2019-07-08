"""
    Google drive core

    This file contains core features for the Google drive utilities
"""

from oauth2client import file, client, tools
from googleapiclient.discovery import build

from gdconstants import print_error_and_exit
from gdconfig import GDConfig

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
    config = GDConfig()
    driver = authenticate(
        config['token_path'],
        config['client_secrets_path'],
        config['scopes'])
    return driver


def get_list(folder='root'):
    """ returns the list of files in the given folder
        @param folder: str containing the Google Drive id of a folder
    """
    fields = 'files(id,name,mimeType)'
    result = get_driver().files().list(
        q="'" + folder + "' in parents and trashed=false",
    ).execute()
    return result['files'] if 'files' in result else []


def get_file(filename, folder='root'):
    """ returns the requested file """
    fields = 'files(id,name,mimeType)'
    result = get_driver().files().list(
        q="name='%s' and '%s' in parents and trashed=false" % (filename, folder),
        spaces='drive',
        fields=fields
    ).execute()
    return result['files'] if 'files' in result else []


def is_folder(filespec):
    """ returns true if filespec specifies a folder
        @param filespec: is one file representation obtained from the driver.
                         It is a dict
        In case filespec doesn't contain key 'mimeType', it returns False
    """
    if not 'mimeType' in filespec:
        return False
    return filespec['mimeType'] == 'application/vnd.google-apps.folder'

if __name__ == "__main__":
    print_error_and_exit('This file is not intended to run alone')
