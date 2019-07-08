#########
ToDo List
#########

Currently
=========

On path testing

- (fixed) gdcli_ls is broken

  ::

    Traceback (most recent call last):
      File "gdcli_ls.py", line 58, in <module>
        main()
      File "gdcli_ls.py", line 55, in main
        do_ls(sys.argv[1:])
      File "gdcli_ls.py", line 48, in do_ls
        files = get_list(get_pwd())
      File "/home/moises/dev/gdcli/src/gdcore.py", line 45, in get_list
        fields=fields
      File "/home/moises/.local/lib/python3.5/site-packages/googleapiclient/_helpers.py", line 130, in positional_wrapper
        return wrapped(*args, **kwargs)
      File "/home/moises/.local/lib/python3.5/site-packages/googleapiclient/http.py", line 851, in execute
        raise HttpError(resp, content, uri=self.uri)
    googleapiclient.errors.HttpError: <HttpError 404 when requesting https://www.googleapis.com/drive/v3/files?fields=files%28id%2Cname%2CmimeType%2Csize%2CfileExtension%29&q=%27%2F%27+in+parents+and+trashed%3Dfalse&alt=json returned "File not found: .">



To Do List
==========

- test_gdpath should mock gdstatus since it is getting pwd from there!

- gdpath.py

  This module should allow translation from nix like paths to gd like
  paths (i.e. ids)

- improve gdcli_cd.py

  it should be able to store current folder somewhere, including the path from
  root (remember this filesystem is not hierarchical)

  a new module dealing with paths is required: gdpath.py

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

- robustness: there's a problem in gdconfig. It could break if a non
  jsonable value is added to a key. Check the XXX in the file

- add color to the output (e.g. {.folder} could appear in a different color when ls

Future
======

This might be dreaming but a further upgrade of this software could be:

- allow dealing with multiple accounts

- integration with ``nautilus``
