#########
ToDo List
#########

Currently
=========

- create gdcli_cd.py

  it should be able to store current folder somewhere, including the path from
  root (remember this filesystem is not hierarchical)

- working on gdcli_ls.py

  - add arguments that allow

    selecting folders to list
    regex to filter
    information to be shown: currently name, extension and size
    way to map human folder and file names to gd ids. See https://developers.google.com/drive/api/v3/search-files

- create the hub gdcli.py that allows arguments for the different utilities
  (e.g. gdcli_ls.py mydir -> $ gdcli ls mydir)


