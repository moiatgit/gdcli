################
Google Drive CLI
################

This repository contains my attempt to create a CLI for the Google Drive

It was inspired by `hschauhan's <https://github.com/hschauhan/gosync>`_ project.

Currently it is in development phase

If I find the time to make it usable, I'll complete this documentation.

Available commands
==================

Since this project is on development, the following list of commands is probably
incomplete and/or imprecise. However, I think it could give you an idea of what
I'm trying to develop.

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



License
=======

You can do whatever you want with the contents of this project under the terms
of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or any later version (your choice)
