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


if __name__ == "__main__":
    print_error_and_exit('This file is not intended to run alone')
