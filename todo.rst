#########
ToDo List
#########

Currently
=========

Current problem:

- queries with names containing special characters (including whitespaces) are
  not working.

  Trying to sanitize them didn't work. The proposed solution is to get the
  contents of each folder and select the names from the client side.

  This try would go quite close to the cache feature. Therefore, it will be
  tackled next

  Cache will be implemented as a sort of filesystem (GDFS.GDFilesystem) that
  will be able to keep a representation of the known GD structure.

  gdfs will offer the functionality currently at gdapi. Everytime a query
  requires something still out of cache, it will query the API and store the
  new information.

  It won't store fisical files. Future download will go by another path

  It won't offer explicit adding of files. Future uploads will go by another
  path

  GDItems that are folders optionally presenting keys 'subfolders' and
  'regularContents'


  steps:

  - (done) create gdfs.py that is able to get a cache of the GD struct

  - (done) Some sort of hierarchical structure of GDItem 

  - turn FS into a singleton: you can use gdsession to keep the only copy as
    in gdapi

  - gdapi calls to API should come always (or mostly) from gdfs

  - gdfs should deliver the information to its users so they don't require
    to access directly to gdapi nor know whether the required information was
    cached or fresh

  - gdfs must allow clearing cache or/and optional params in its operations to
    get fresh values

    An option --non-cache could force any command to access directly to GD

    A command refresh or clear_cache could refresh/clear cache info

  - review gditem's new operations to be tested!

  - update gditem, gdpath so they work using gdfs

To Do List
==========

- consider moving gdpath.items_from_path to gdfs

- consider moving fixtures from test_gdpath and test_gdcli_ls to utiltest

- gdcli_about is using directly the GD driver. All API queries should be
  encapsulated in a single module (i.e. gdapi.py)

- complete gdcli_cd.py

  it should be able to change the status values (and store them!)

- add version notice (e.g. gdcli v0.1) it could go in a settings file or
  similar

- improve gdcli_ls.py

  - add arguments that allow

    - regex (or at least * ) to path

      xpath could be also an option

      at least consider // notation for searching in any subfolder

    - information to be shown: i.e. name, extension and size

      it could be perfomed by another command (e.g. gdcli_info)

- create the hub gdcli.py that allows arguments for the different utilities
  (e.g. gdcli_ls.py mydir -> $ gdcli ls mydir)

  Consider naming the hub as gd for simplicity

- other commands:

  - download file

    proposed command

    $ gdcli download gd/path/to/file [local/path/to/destination]

    Special case: the file is already downloaded

    There're a bunch of things to take into account here: formats (save as), update, …

  - rename (strictly changing the name of a file)

  - move (move a file from one folder to another)

  - remove (move a file to trash)

  - upload (upload a file from local filesystem)

    Similar issues of download with formats (upload as) and possible problems
    with multiple folders

  - mkdir (create a new folder)

- robustness: there's a problem in gdconfig. It could break if a non
  jsonable value is added to a key. Check the XXX in the file

- consider coverall or any other tool to check coverage

  - https://coveralls.io/sign-up

- consider implementing singleton as metaclasses

  https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python

- consider adding type info when ls
    if item['mimeType'] == 'msword' and not (
        item['name'].tolower().endswith('doc') or
            item['name'].tolower().endswith('docx')
    ):
        return full_path + '{.doc}'

    _MIMETYPE_TO_EXTENSION_MAPPINGS = {
        'application/msword': 'msword',
        'application/pdf': 'pdf',
        'image/jpeg': 'jpeg',

        'application/vnd.google-apps.audio': 'audio',
        'application/vnd.google-apps.document': 'Google Docs',
        'application/vnd.google-apps.drawing': 'Google Drawing',
        'application/vnd.google-apps.file': 'Google Drive file',
        'application/vnd.google-apps.folder': 'Google Drive folder',
        'application/vnd.google-apps.form': 'Google Forms',
        'application/vnd.google-apps.fusiontable': 'Google Fusion Tables',
        'application/vnd.google-apps.map': 'Google My Maps',
        'application/vnd.google-apps.photo': 'Google photo',
        'application/vnd.google-apps.presentation': 'Google Slides',
        'application/vnd.google-apps.script': 'Google Apps Scripts',
        'application/vnd.google-apps.site': 'Google Sites',
        'application/vnd.google-apps.spreadsheet': 'Google Sheets',
        'application/vnd.google-apps.unknown': 'unknown',
        'application/vnd.google-apps.video': 'Google Video',
        'application/vnd.google-apps.drive-sdk': 'Google 3rd party shortcut',
    }

    def test_print_item_when_known_extension():
        item = gditem.GDItem('/one/itemname', ['root', 'oneid', 'itemnameid'],
                             'application/pdf')
        expected = '/one/itemname{.pdf}'
        got = gdcli_ls.item_to_str(item)
        assert got == expected


- add color to the output (e.g. {.doc} could appear in a different color when ls

- consider if gdconstants is a proper name for a bunch of constants PLUS some utilitiy methods

- gdcli_ls consider moving _MIMETYPE_TO_EXTENSION_MAPPINGS to a configuration file so it can get updated without reprogramming

  It will make sense when implementing further information about each entry on
  ls command. By now, the only special information for ls output is adding a /
  to folders


Future
======

This might be dreaming but a further upgrade of this software could be:

- allow dealing with multiple accounts

- integration with ``nautilus``
