"""
ffs.util

General utilities for working with filesystems
"""
from __future__ import with_statement

import os
import re
from _functools import partial

from six.moves import StringIO

def _defensive_dperms(filename):
    """
    Check that the permissions of `filename`'s directory are sane

    Arguments:
    - `filename`: str

    Return: bool
    Exceptions: None
    """
    filename = os.path.abspath(filename)
    targetdir = os.path.dirname(filename)
    if not os.path.isdir(targetdir):
        return False
    return True

def _defensive_access(filepath):
    """
    Defensively check for access to filepath

    Arguments:
    - `filepath`: str

    Return: bool
    Exceptions: None
     """
    filepath = os.path.abspath(filepath)
    if not _defensive_dperms(filepath):
        return False
    if not os.path.exists(filepath):
        return False
    return True

def is_dir(path):
    """
    Predicate to determine if PATH is an existng directory

    Arguments:
    - `path`: str or Path

    Return: bool
    Exceptions: None
    """
    return os.path.isdir(str(path))

def is_file(path):
    """
    Predicate to determine if PATH is an existng file

    Arguments:
    - `path`: str or Path

    Return: bool
    Exceptions: None
    """
    return os.path.isfile(str(path))

def hsize(filepath):
    """
    Return the size of the file at `filepath` as a hex string
    or None if the file does not exist/is not accessible, printing
    an appropriate warning.

    Arguments:
    - `filepath`: str

    Return: str
    Exceptions: None
    """
    filename = os.path.abspath(filepath)
    fsize = size(filepath)
    if fsize:
        return hex(fsize)
    return None

def size(filepath):
    """
    Return the integer value of the size of `filepath' in bytes

    Arguments:
    - `filepath`: str

    Return: int
    Exceptions: None
    """
    filename = os.path.abspath(filepath)
    if not _defensive_access(filepath):
        return None
    return int(os.stat(filename).st_size)

class Flike(StringIO):
    "String IO that understands the Contextmanager protocol"
    def __enter__(self):
        return self

    def __exit__(self, msg, val, tb):
        return


#
# We backport the 3.3 implementation of functools.wraps
# as of changeset:   75186:31784350f849
# This allows us to use wraps on methods.
#


WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__qualname__', '__doc__',
                       '__annotations__')
WRAPPER_UPDATES = ('__dict__',)
def update_wrapper(wrapper,
                   wrapped,
                   assigned = WRAPPER_ASSIGNMENTS,
                   updated = WRAPPER_UPDATES):
    """Update a wrapper function to look like the wrapped function

       wrapper is the function to be updated
       wrapped is the original function
       assigned is a tuple naming the attributes assigned directly
       from the wrapped function to the wrapper function (defaults to
       functools.WRAPPER_ASSIGNMENTS)
       updated is a tuple naming the attributes of the wrapper that
       are updated with the corresponding attribute from the wrapped
       function (defaults to functools.WRAPPER_UPDATES)
    """
    wrapper.__wrapped__ = wrapped
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    # Return the wrapper so this can be used as a decorator via partial()
    return wrapper

def wraps(wrapped,
          assigned = WRAPPER_ASSIGNMENTS,
          updated = WRAPPER_UPDATES):
    """Decorator factory to apply update_wrapper() to a wrapper function

       Returns a decorator that invokes update_wrapper() with the decorated
       function as the wrapper argument and the arguments to wraps() as the
       remaining arguments. Default arguments are as for update_wrapper().
       This is a convenience function to simplify applying partial() to
       update_wrapper().
    """
    return partial(update_wrapper, wrapped=wrapped,
                   assigned=assigned, updated=updated)
