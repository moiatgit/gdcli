#! /usr/bin/env python3

"""
    Google Drive CLI: help

    This script offers general help to use gdcli suite
"""
import sys

_GENERAL_HELP = (
        'Google Drive CLI: help',
        '',
        'gdcli is a script that allows you to access your',
        'Google Drive contents from command line.',
        'usage: gdcli <command>',
        'For help on an specific command use: gdcli help <command>',
        '',
        'General commands are:',
        'help:\tshows this help',
        'about:\tshows general information about your drive account',
        'start:\tchecks and helps setting up the installation of gdcli',
        '',
        'Files and folders commands are:',
        'ls:\tshows file contents of Google Drive current working directory',
        'pwd:\tshows the current working directory',
        'cd:\tchanges the Google Drive current working directory',
        'info:\tshows verbose information about a file in Google Drive',
        '',
        'Local files',
        'download:\tdownloads a Google Drive file',
        'upload:\tuploads a local file to Google Drive',
        'compare:\tcompares a Google Drive file with a local copy',
        )

def show_general_help():
    """ shows general help """
    for line in _GENERAL_HELP:
        print(line)

def do_help(argv):
    """ shows help.
        @argv is a list of str arguments """
    if argv:
        print('WARNING: specific help about a command is not available yet\n')
    show_general_help()


def main():
    """ shows the help """
    do_help(sys.argv[1:])

if __name__ == '__main__':
    main()
