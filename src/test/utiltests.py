"""
    Google Drive CLI: utility functions for testing
"""

def build_mock_get(contents):
    """ given a list of contents to be return by a sequence of mocked calls
        it returns a function that will deliver each entry of the contents """

    def generator(contents):
        for c in contents:
            yield c
    gen = generator(contents)


    def mock_get(*args, **kwargs):
        nonlocal gen
        return next(gen)

    return mock_get


