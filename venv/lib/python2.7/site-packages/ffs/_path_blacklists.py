"""
ffs._path_blacklists

To avoid editing two lists of methodnames when we change the Path ducktyping (test and code),
we maintan the blacklists here.
"""
_strblacklist = [
            'capitalize',
            'center',
            'count',
            'encode',
            'expandtabs',
            'format',
            'index',
            'isalnum',
            'isalpha',
            'isdigit',
            'islower',
            'isspace',
            'istitle',
            'isupper',
            'join',
            'ljust',
            'lower',
            'lstrip',
            'partition',
            'replace',
            'rindex',
            'rjust',
            'rsplit',
            'splitlines',
            'swapcase',
            'title',
            'translate',
            'upper',
            'zfill',
            'isnumeric',
            'isdecimal',
            ]
