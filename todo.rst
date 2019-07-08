#########
ToDo List
#########

Currently
=========

- (done) testing case existing file (not folder) as a step in the path


To Do List
==========

- (done) test_gdpath should mock gdstatus since it is getting pwd from there!

- (done) gdpath.py

  This module should allow translation from nix like paths to gd like
  paths (i.e. ids)

- improve gdcli_cd.py

  it should be able to store current folder somewhere, including the path from
  root (remember this filesystem is not hierarchical)

  most probably it will require asking to gdpath specifically for a folder

  (done) a new module dealing with paths is required: gdpath.py

- add version notice (e.g. gdcli v0.1) it could go in a settings file or
  similar

- working on gdcli_ls.py

  - add arguments that allow

    (done) selecting folders to list
    regex to filter
    information to be shown: currently name, extension and size
    way to map human folder and file names to gd ids. See https://developers.google.com/drive/api/v3/search-files

- move gdcli_pwd.get_pwd_id() and get_pwd() to gdstatus

- create the hub gdcli.py that allows arguments for the different utilities
  (e.g. gdcli_ls.py mydir -> $ gdcli ls mydir)


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
