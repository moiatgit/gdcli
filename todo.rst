#########
ToDo List
#########

Currently
=========

Current problem:

- there's a problem with gdpath: it returns the item id only but I'd need
  also whether it is a folder or not.

  I've created gdpath.GDItem to allow keeping this information all the time

  At this moment I'm converting test_gdpath

  Further tasks will involve to get pwd as a GDItem



To Do List
==========

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
