#########
ToDo List
#########

Currently
=========

- simplify gdconfig so it:

  - (done) always takes settings from ~/.gdcli


To Do List
==========

- (done) create gdcli_help

  start with basic help

- gdcli_pwd

- (done) create gdcli_start.py

  It should guide the user to configure the app

  - check whether ~/.gdcli exists

  - check client_secrets.json

  - check token or launch to get it

    (dismissed) This could simplify current code since gdcore.py authorize() is
    checking for this token and launching the browser in case there's a problem.
    New workings could be just to issue an error asking to run
    ``gdcli_start.py``

- create gdcli_cd.py

  it should be able to store current folder somewhere, including the path from
  root (remember this filesystem is not hierarchical)

- add version notice (e.g. gdcli v0.1) it could go in a settings file or
  similar

- working on gdcli_ls.py

  - add arguments that allow

    selecting folders to list
    regex to filter
    information to be shown: currently name, extension and size
    way to map human folder and file names to gd ids. See https://developers.google.com/drive/api/v3/search-files

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

- (done) remove redundancy: redefinition of default gdconfig file path in gdcli_start
  and gdconfig


Future
======

This might be dreaming but a further upgrade of this software could be:

- allow dealing with multiple accounts

- integration with ``nautilus``
