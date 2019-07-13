#########
ToDo List
#########

Currently
=========

Current problem:

- names in GD can contain / so it doesn't work when trying to split by slash
  proposal 1: store all item names in a list and use paths with its position
              session names

  gdcore._gdcontents_to_gditem() seems to not generate GDItem with full path.
  It must be created a test_gdcore mocking the API calls. In fact, they're already encapsulated in just one
  method gdcore._get_items() so you just have to mock this one. Get sure you check the args of the call
  so they correspond to the expected query and folder

  Currently it is required to mock Session

  Just thinking: Session is getting too complex to test. Wouldn't it be possible that GDItem contains all the information
  about its original names and offer methods to avoid use of split()? The main difficulty on this approach is to manipulate
  nix paths as received by the command (e.g. ls) but you won't scape from this even with the Session mechanism fully working

  The problem with slashes at nixpaths could be solved with the standard scape mechanism. i.e. '\/' is a non-path-separator slash and '\\' is a non-escape inverted slash

  Consider defining a test case of a file with steps including slashes

  Let's create a new branch to replace Session by this idea:
  - GDItem.named_path as list of names (this avoids split('/') requirement on GDItem
  - gdpath offers nixpath_to_gdpath() and gdpath_to_nixpath() methods
  - Session will just keep the driver by now

To Do List
==========

- check whether the testing with set[GDItem] actually work

- (done) Further tasks will involve to get pwd as a GDItem

- consider moving gdpath.items_from_path to gdcore

- important optimization

  currently, each time gdcli access to GD, it requires authentication!
  (done) Change it to a singleton or something so it can share the same driver during all the process life!
  Test it!

- gdcli_ls consider moving _MIMETYPE_TO_EXTENSION_MAPPINGS to a configuration file so it can get updated without reprogramming

- gditem.proper_paths() should conform to other checkings in the standard library
  for example, list.join() calls to _check_arg_types() that, on error,
    raise TypeError('named path must be absolute')
  Get sure you test it at test_gditem

- consider moving fixtures from test_gdpath and test_gdcli_ls to utiltest

- ls has some issues:

  - it seems unable to list a concrete file

    The problem is that gdcore-get_list() are looking for parents not for filenames
    Therefore, on empty result, it should look for the name of the file in the parent. It should be possible to check for the basedir of the path as folder
    Another option (of loosers) is to discard this functionality and just allow listing folders

  - it shows the type even for the known file extensions. e.g. file.pdf{.pdf}

  - (done) it shows the title of the script for each passed argument

  - it breaks when a missing file is required

- gdcore get_list() and get_file() do practically the same. Refactor!

- improve gdcli_cd.py

  it should be able to store current folder somewhere, including the path from
  root (remember this filesystem is not hierarchical)

  most probably it will require asking to gdpath specifically for a folder

- add version notice (e.g. gdcli v0.1) it could go in a settings file or
  similar

- working on gdcli_ls.py

  - folders could be marked ending with slash

  - add arguments that allow

    - regex (or at least *) to path

    - information to be shown: i.e. name, extension and size

- move gdcli_pwd.get_pwd_id() and get_pwd() to gdstatus

- create the hub gdcli.py that allows arguments for the different utilities
  (e.g. gdcli_ls.py mydir -> $ gdcli ls mydir)

- consider adding cache features

  i.e. store the folder struct and even the GD files' info, so you can reach them directly

  An option --non-cache could force any command to access directly to GD

  A command refresh or clear_cache could refresh/clear cache info

- other commands:

  - download file

    proposed command

    $ gdcli download gd/path/to/file [local/path/to/destination]

    Special case: the file is already downloaded

  - rename (strictly changing the name of a file)

  - move (move a file from one folder to another)

  - remove (move a file to trash)

  - upload (upload a file from local filesystem)

- robustness: there's a problem in gdconfig. It could break if a non
  jsonable value is added to a key. Check the XXX in the file


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

Future
======

This might be dreaming but a further upgrade of this software could be:

- allow dealing with multiple accounts

- integration with ``nautilus``
