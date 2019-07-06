#! /usr/bin/env python3

"""
    google drive cli: about

    This script shows the information about the drive
"""

from gdcore import get_driver


# Description of the data to be shown
_ABOUT_SPECS = [
    {'name':'user_name', 'text': 'display name', 'key': 'user',
     'subkey': 'displayName', 'type': 'text'},
    {'name': 'user_email', 'text': 'email', 'key': 'user',
     'subkey': 'emailAddress', 'type': 'text'},
    {'name': 'quota_usage', 'text': 'bytes in use', 'key': 'storageQuota',
     'subkey': 'usage', 'type': 'numeric'},
    {'name': 'quota_in_drive', 'text': 'bytes in drive', 'key': 'storageQuota',
     'subkey': 'usageInDrive', 'type': 'numeric'},
    {'name': 'quota_in_trash', 'text': 'bytes in trash', 'key': 'storageQuota',
     'subkey': 'usageInDriveTrash', 'type': 'numeric'},
    {'name': 'import_limit_drawings', 'text': 'import limit for drawings',
     'key': 'maxImportSizes', 'subkey': 'application/vnd.google-apps.drawing',
     'type': 'numeric'},
    {'name':'import_limit_documents', 'text': 'import limit for documents',
     'key': 'maxImportSizes', 'subkey': 'application/vnd.google-apps.document',
     'type': 'numeric'},
    {'name':'import_limit_spreadsheets', 'text': 'import limit for spreadsheets',
     'key': 'maxImportSizes', 'subkey': 'application/vnd.google-apps.spreadsheet',
     'type': 'numeric'},
    {'name':'upload_limit', 'text': 'upload limit', 'key': 'maxUploadSize',
     'type': 'numeric'},
]


# XXX consider moving drive calls to gdcore so this script is independent of drive
def get_about(drive):
    """ returns the information about the drive filtered by _ABOUT_SPECS.
        The returning value is a list of dicts as return in compose_values()
    """
    fields = 'storageQuota,user,maxImportSizes,maxUploadSize'
    raw_about = drive.about().get(fields=fields).execute()
    about = add_values(raw_about)
    return about


def add_values(about):
    """ given the about info, it returns a list where each item contains a new field
        named 'value' according to the _ABOUT_SPECS specs

    """
    result = []
    for item in _ABOUT_SPECS:
        value = compose_value(item, about)
        valued_item = dict(item)
        valued_item['value'] = value
        result.append(valued_item)
    return result


def compose_value(item, about):
    """ Given an item spec, it returns the corresponding value from the about info """
    if 'subkey' in item:
        value = about[item['key']][item['subkey']]
    else:
        value = about[item['key']]
    return value


def format_number(text):
    """ converts a text to a nice number """
    return '{:,}'.format(int(text))


def prettify_value(about_value):
    """ given a value it returns its corresponding value in a nice form """
    value = about_value['value']
    if about_value['type'] == 'numeric':
        value = format_number(int(value))
    return value


def print_about(values):
    """ prints the rellevant information about the drive to the standard output
        @param values: a list of dict with keys 'name', 'type', and 'value'
    """
    print('Google Drive CLI: about')
    for item in values:
        value = prettify_value(item)
        print('%30s: %s' % (item['text'], value))

def main():
    """ performs the interactive task of this module
        It shows the about information of the Google Drive """
    driver = get_driver()
    about = get_about(driver)
    print_about(about)

if __name__ == '__main__':
    main()
