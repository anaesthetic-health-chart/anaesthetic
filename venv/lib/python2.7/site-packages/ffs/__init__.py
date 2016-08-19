
"""
Filesystem API helpers
"""
from __future__ import with_statement

import datetime
import errno
import os
import sys

from ffs import exceptions, formats, nixargs
from ffs.util import is_dir, is_file, hsize, size
from ffs.nix import (cd, chmod, chown, cmp,
                     cp, cp_r,
                     getwd,
                     ln, ln_s,
                     ls,
                     mkdir, mkdir_p, mv,
                     pwd,
                     rm, rmdir, rm_r,
                     stat,
                     touch, unlink, which,
                     is_exe)
from ffs.path import Path
from ffs._version import __version__

ts2dt = datetime.datetime.utcfromtimestamp

if sys.platform.startswith("win"):
    OS = "WINDOWS!"
else:
    OS = "LINUX!"

__all__ = [
    '__version__'
    # Modules
    'exceptions',
    'formats',
    'nixargs',
    # Nix helpers
    'cd',
    'chmod',
    'chown',
    'cmp',
    'cp',
    'cp_r',
    'getwd',
    'ln',
    'ln_s',
    'mkdir',
    'mkdir_p',
    'mv',
    'pwd',
    'rm',
    'rmdir',
    'rm_r',
    'stat',
    'touch'
    'unlink',
    'which',
    # Predicates
    'is_exe',
    'is_dir',
    'is_file',
    # Filesystem helpers
    'size',
    'hsize',
    # Path
    'Path',
    ]

def basen(path, num=1):
    """
    Return the last `num` components of `path`

    Arguments:
    - `path`: str
    - `num`: int

    Return: str
    Exceptions: None
    """
    # Almost certainly a faster algorithm for this.
    # See testcase in test_fs for expected results
    return os.sep.join(list(reversed([e for i, e in enumerate(reversed(path.split(os.sep))) if i < num])))

def lsmtime(path, lessthan=None):
    """
    Return a list of all files existing in `path`
    where their mtime is less than `lessthan`.

    The return is a list of strings which are absolute paths
    to the files.

    Arguments:
    - `path`: str
    - `lessthan`: DateTime

    Return: [str,]
    Exceptions: None
    """
    for base, dirs, files in os.walk(path):
        ls = []
        for fname in files:
            fpath = os.path.join(base, fname)
            # Don't rely on os.stat_float_times() == True
            mtime = float(os.path.getmtime(fpath))
            if ts2dt(mtime)< lessthan:
                ls.append(fpath)
        return ls
