"""
    Google Drive CLI: utility functions for testing
"""

def build_mock_get(contents, expected_args=None, expected_kwargs=None):
    """ given a list of contents to be return by a sequence of mocked calls
        it returns a function that will deliver each entry of the contents """

    def generator(contents):
        for c in contents:
            yield c
    gen = generator(contents)


    def mock_get(*args, **kwargs):
        nonlocal gen
        if expected_args:
            assert args == expected_args, "Expected args %s but found %s" % (args, expected_args)
        if expected_kwargs:
            assert kwargs == expected_kwargs, "Expected kwargs %s but found %s" % (kwargs, expected_kwargs)
        return next(gen)

    return mock_get


