"""
    Google Drive status

    This module encapsulates dealing with status
"""
import os

from gdconstants import _STATUS_FILENAME_EXPANDED, print_error_and_exit
from gdconfig import GDConfig

def get_status():
    """ tryies to get the status file and loads it as a GDConfig
        If the status file is not present, it creates one with default
        information.
    """
    def create_status_file_if_necessary():
        if not os.path.exists(_STATUS_FILENAME_EXPANDED):
            with open(_STATUS_FILENAME_EXPANDED, "w") as f:
                f.write('{}')
    def add_pwd_if_necessary(status):
        if not 'pwd' in status:
            status['pwd'] = 'root'
            status.store()

    create_status_file_if_necessary()
    status = GDConfig(_STATUS_FILENAME_EXPANDED)
    add_pwd_if_necessary(status)
    return status

if __name__ == '__main__':
    print_error_and_exit('This file is not intended to run alone')
