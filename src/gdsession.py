"""
    Google Drive session

    This file contains a class that encapsulates different values of the current
    session
    - the reference to the driver

"""

class Session:
    """ encapsulates the information about the current session """
    _instance = dict()

    @staticmethod
    def get_driver():
        """ returns the session driver. If unknown, it raises an exception """
        if 'driver' not in Session._instance:
            raise Exception('driver unknown')
        return Session._instance['driver']

    @staticmethod
    def set_driver(driver):
        """ sets the session driver. If already set, it raises an exception """
        if 'driver' in Session._instance:
            raise Exception('driver already set')
        return Session._instance.setdefault('driver', driver)

    @staticmethod
    def is_driver():
        """ returns True when the driver is set """
        return 'driver' in Session._instance

