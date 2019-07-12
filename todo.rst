#########
ToDo List
#########

Currently
=========

Current problem:

- (done) since it is possible that more of one entry has the same name in the same folder, it is also possible that:

  - there's a folder and a file equally named and the folder contains the required file. So I must search on every possible folder

  - two folders equally named, one contains the required file and the other doesn't

  - these cases could happen in any step in the path

  For this reason, the following changes must be considered:

  - (done) gdpath.named_path_to_gditem() must return (list[GDItem], msg)

  - (done) recursive gdpath.named_path_to_gditem()

  - (done) for simplicity, there will be considered only one type of error: no items found
    That implies no GDPath is required

- (done) there's a problem with gdpath: it returns the item id only but I'd need
  also whether it is a folder or not.

  I've created gdpath.GDItem to allow keeping this information all the time

  (done) At this moment I'm converting test_gdpath

- (done) rename path_to_gd() to named_path_to_gditem()

- (done) There're some non yet converted tests for path

- (done) There're also two new tests to be defined. They have to do with the fact that it is possible to get two files with the same name in GD.
  It will require to decide whether to present everything, which one to keep (for mimeType decisions)
  It will also make more complex ls and make it more appealing to require ls path/to/folder/ end by slash if user wants to list folder contents

- (done) replace calls to old query methods on gdcore to the new ones (e.g. get_file() to get_items_by_name())
  Start with test_gdpath

- Further tasks will involve to get pwd as a GDItem

- consider moving gdpath.items_from_path to gdcore


To Do List
==========

- important optimization

  currently, each time gdcli access to GD, it requires authentication!
  (done) Change it to a singleton or something so it can share the same driver during all the process life!
  Test it!

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

- add color to the output (e.g. {.folder} could appear in a different color when ls

Future
======

This might be dreaming but a further upgrade of this software could be:

- allow dealing with multiple accounts

- integration with ``nautilus``
