################
Google Drive CLI
################

This repository contains my attempt to create a CLI for the Google Drive

It was inspired by `hschauhan's <https://github.com/hschauhan/gosync>`_ project.

Currently it is in development phase

If I find the time to make it usable, I'll complete this documentation.

Installation
============

If you are interested in running this project, you can just clone this repo and
install the dependencies.

I'm using Python 3.5 because it comes pre-installed in my OS. I would propose
you to use some virtualization mechanism (e.g. ``virtualenv``) but, if you aren't
involved in too many projects, you might want to install the dependencies at
your user folder.

Instructions could go something like:

::

    $ cd whereveryouwanttokeeptit/
    $ git clone https://github.com/moiatgit/gdcli
    $ cd gdcli
    $ pip3 install --user -Ur requirements.txt


Available commands
==================

Since this project is on development, the following list of commands is most
probably incomplete and/or imprecise. However, I think it could give you an idea
of what I'm trying to develop.

Start
-----

Check whether your installation is successfully configured

::

    $ python3 gdcli_start.py

    Google Drive CLI: initial configuration utility

    Congratulations. Your Google Drive CLI is ready for use
    Tip: to continue consider getting some help
    $ gdcli help

About
-----

Get information of your Google Drive:

::

    $ python3 gdcli_about.py
    Google Drive CLI: about
                      display name: Moisès Gómez
                             email: myaddress@gmail.com
                      bytes in use: 2,734,568,974
                    bytes in drive: 236,776,984
                    bytes in trash: 84,909,334
         import limit for drawings: 2,097,152
        import limit for documents: 10,485,760
     import limit for spreadsheets: 104,857,600
                      upload limit: 5,242,880,000,000


List contents
-------------

Get the contents of a folder in your Google Drive:

::

    $ python3 gdcli_ls.py /folder1
    Google Driver CLI: ls
    file1.pdf
    file2.pdf
    folder11{.folder}

    total files: 3

Current version is able to accept multiple and complex paths as arguments of
this command.

There's a known issue, however: when querying for names with special characters,
it doesn't get the expected response.

Contribute
==========

So you find this project interesting enough to expend some time on it? That's great!

Since I'm the only developer here (AFAIK) I'm not investing too much in breaking
the remaining tasks into assignable pieces. However, there's the file
``todo.rst`` that contains the list of To Do. I'm trying to keep it reasonably
updated, so you can fork this repo, pick up one of the tasks in the list (not
prefixed by ``(done)``) and do your best! I think, though, that it would be more
productive if you just drop me an email and we talk about it first.

I'm developing on local branches, so the master contains something acceptably
stable.

Thanks for your interest!

License
=======

You can do whatever you want with the contents of this project under the terms
of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or any later version (your choice)
