"""
    Google Drive session

    This file contains a class that encapsulates different values of the current
    session
    - the reference to the driver
    - the item name's

"""

class Session:
    """ encapsulates the information about the current session """
    _instance = {
        'names': {},
        'representations': {}
    }

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

    @staticmethod
    def add_name(name):
        """ adds a new item name to the known item names for this session.
            It returns the representation of this name. A unique str value in this
            session
            If the name is already known, it returns its corresponding representation.
        """
        names = Session._instance['names']
        representation = names.setdefault(name, str(len(names)))
        representations = Session._instance['representations']
        representations.setdefault(representation, name)
        return representation

    @staticmethod
    def get_representation(name):
        """ returns the representation of a name.
            If it is unknown, it raises an exception """
        return Session._instance['names'][name]

    @staticmethod
    def get_name(representation):
        """ returns the name corresponding to the representation
            If it is unknown, it raises an exception """
        return Session._instance['representations'][representation]

    @staticmethod
    def get_path_from_representation(representation_path):
        """ given a nix-like path of representations, it returns
            the path with each step translated """
        print("XXX get_path_from_representation(%s)" % representation_path)
        path_splitted = representation_path.split('/')
        translations = [Session.get_name(repr) if repr else '/' for repr in path_splitted]
        return '/'.join(translations)
