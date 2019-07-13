"""
    Google drive core

    This file contains core features for the Google drive utilities
"""

import os
from oauth2client import file, client, tools
from googleapiclient.discovery import build
from urllib.parse import quote

import gdconstants
import gdconfig
import gditem
import gdsession

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
        It will construct the driver once in this session, so it will store in
        Session
        It has into account the settings in GDConfig.
    """
    if not gdsession.Session.is_driver():
        config = gdconfig.GDConfig()
        driver = authenticate(
            config['token_path'],
            config['client_secrets_path'],
            config['scopes'])
        gdsession.Session.set_driver(driver)
    return gdsession.Session.get_driver()


def _gdcontents_to_gditem(contents, folder):
    """ given a response of a Google Drive query, it return the list
        of GDItem contained in the 'files' entry if present

        @param contents: a dict as return by a query to Google Driver
        @param folder: a GDItem such that folder.is_folder() == True
        @return list[GDItem]
    """
    items = []
    for raw_item in contents.get('files', []):
        name = raw_item['name']
        item = gditem.GDItem(
            folder['namedPath'] + [name],
            folder['idPath'] + [raw_item['id']],
            raw_item['mimeType'])
        items.append(item)
    return items


def _get_raw_items(query):
    """ it returns the contents mathing the query as returned by the API """
    fields = 'files(id,name,mimeType)'
    result = get_driver().files().list(
        q=query,
        spaces='drive',
        fields=fields
    ).execute()
    return result


def _get_items(query, folder):
    """ returns the contents matching the query as a list of GDItem """
    raw_items = _get_raw_items(query)
    return _gdcontents_to_gditem(raw_items, folder)


def get_items_by_name(name, folder):
    """ it returns the contents from folder with the given name.
        Note: Google Drive allows multiple files equally named in the same folder!

        @param name: str defining the name of the item to find
        @param folder: a GDItem such that folder.is_folder() == True
        @return list[GDItem]
    """
    parent = folder['id']
    sanitized_name = quote(name)
    query = "name='%s' and '%s' in parents and trashed=false" % (sanitized_name, parent)
    return _get_items(query, folder)


def get_items_by_folder(folder):
    """ it returns the contents from folder
        @param folder: a GDItem such that folder.is_folder() == True
        @return list[GDItem]
    """
    parent = folder['id']
    query = "'%s' in parents and trashed=false" % parent
    return _get_items(query, folder)


if __name__ == "__main__":
    gdconstants.print_error_and_exit('This file is not intended to run alone')
