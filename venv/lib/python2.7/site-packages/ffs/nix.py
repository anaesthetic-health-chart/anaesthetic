"""
*nix style python functions
"""
from __future__ import with_statement

import contextlib
import errno
import filecmp
import grp
import os
import pwd as pwdb
import shutil
import sys

from ffs import exceptions

class cd(object):
    """
    Change directory to PATH. Mimics the *nix cd command

    When used as a contextmanager, will change directory
    within the nested block, returning you to your previous
    location on exit. Yields a Path object representing the
    new current directory.

    Arguments:
    - `path`: str

    Return: None or Path when contextmanager
    Exceptions: None
    """
    def __init__(self, path):
        """
        Change directories on initialization.
        This is a "Bad idea" but it allows us to be both
        function-like and contextmanager-like
        """
        self.startdir = getwd()
        self.path = path
        os.chdir(str(path)) # Coerce Path objects

    def __enter__(self):
        """
        Contextmanager protocol initialization.

        Returns a Path representing the current working directory
        """
        from ffs import Path
        return Path(self.path)

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Contextmanager handling.return to the original directory
        """
        os.chdir(self.startdir)
        return

# !!! Allow symbolic permissions
def chmod(path, mode):
    """
    Change the access permissions of a file.
    Also accepts Path objects

    Arguments:
    - `path`: str or Path
    - `mode`: int

    Return: None
    Exceptions: None
    """
    return os.chmod(str(path), mode)

# ::chmod_R (FileUtils)

def chown(path, user=None, group=None, uid=None, gid=None):
    """
    Python translation of the *nix chown command.

    When given either a user, a group, or both, change PATH to be owned
    by that user/group/both.

    These can be specified by string via USER and GROUP or by numeric id
    via UID and GID.

    If both USER and UID or both GROUP and GID are passed, raise ValueError
    as we have no way of knowing what you meant.

    If none of USER, UID, GROUP, GID are passed, raise ValueError as this is
    nonsense, and you should be alerted to this so that you can stop doing it.

    Arguments:
    - `path`: str or Path
    - `user`: str
    - `group`: str
    - `uid`: int
    - `gid`: int

    Return: None
    Exceptions: ValueError
    """
    if len([x for x in [user, group, uid, gid] if x is None]) == 4:
        msg = "You haven't given a group or user to change to Larry... "
        raise ValueError(msg)
    if user and uid:
        raise ValueError("It doesn't make sense to set USER and UID Larry... ")
    if group and gid:
        raise ValueError("It doesn't make sense to set GROUP and GID Larry... ")

    _uid, _gid = -1, -1
    if uid is not None:
        _uid = uid
    if gid is not None:
        _gid = gid
    if user is not None:
        _uid = pwdb.getpwnam(user)[2]
    if group is not None:
        _gid = grp.getgrnam(group)[2]
    os.chown(str(path), _uid, _gid)
    return

# ::chown_R (FileUtils)

cmp = filecmp.cmp

def cp(resource, target, recursive=False):
    """
    Python translation of GNU cp.

    Copy RESOURCE to TARGET.
    If RECURSIVE is True and RESOURCE is a directory, copy the tree.
    If RECURSIVE is False and RESOURCE is a directory, a no-op
    If RESOURCE does not exist, raise DoesNotExistError
    If TARGET exists, raise ExistsError

    Arguments:
    - `resource`: str or Path
    - `target`: str or Path
    - `recursive`: bool

    Return: None
    Exceptions: DoesNotExistError, ExistsError
    """
    if not os.path.exists(resource):
        raise exceptions.DoesNotExistError("Can't copy something that doesn't exist Larry... ")
    if os.path.exists(target):
        raise exceptions.ExistsError("Won't overwrite an existing target Larry... ")
    if os.path.isdir(resource):
        if recursive:
            return shutil.copytree(resource, target)
        return
    shutil.copy2(resource, target)
    return

cp_r = shutil.copytree

getwd = os.getcwd

def head(filename, lines=10):
    """
    Python port of the *nix head command.

    Return the frist LINES lines of the file at FILENAME
    Defaults to 10 lines.

    Arguments:
    - `filename`: str or Path
    - `lines`: int

    Return: str
    Exceptions: None
    """
    with open(str(filename)) as fh:
        return "".join(fh.readlines()[:lines])


# ::install (FileUtils)

def ln(src, dest, force=None, symbolic=None):
    """
    Python translation of GNU ln

    Create a link at SRC pointing to DEST.
    If there is a file at DEST, raise ExistsError

    If FORCE is truthy, remove any file at DEST.
    If SYMBOLIC is truthy, make symbolic links instead of hard links.

    Arguments:
    - `src`:
    - `dest`:
    - `force`:
    - `symbolic`

    Return: None
    Exceptions: ExistsError
    """
    if not force and os.path.exists(dest):
        raise exceptions.ExistsError(
            '{0} already exists Larry... did you mean to force?'.format(dest))
    if force and os.path.exists(dest):
        rm(dest)
    if symbolic:
        ln_s(src, dest)
    else:
        os.link(src, dest)
    return

# # !!! Wrap to accept Path objects
# ln = os.link

# # !!! Wrap to accept Path objects
ln_s = os.symlink

# ::ln_sf (FileUtils)

# !!! expand to include other ls flags
def ls(path, all=None, almost_all=None, ignore_backups=None):
    """
    Python translation of GNU ls

    Returns a list of strings representing files and directories
    contained by PATH.

    The list will never contain the special entries '.' and '..' even
    if they are present in the directory.

    By default, the list is in arbitrary order and directories or files
    beginning with '.' are omitted.

    If ALL is truthy, we will not ignore entries starting in '.'
    If ALMOST_ALL is truthy we will not list the implied '.' and '..'
    ALL takes precedence over ALMOST_ALL. Take it up with Stallman.
    If IGNORE_BACKUPS is truthy, we will ignore entries starting in '~'
    IGNORE_BACKUPS takes precedence over ALL. Again, take it up with Stallman.

    Arguments:
    - `path`: str or Path
    - `all`: bool
    - `almost_all`: bool
    - `ignore_backups`: bool

    Return: list[str]
    Exceptions:None
    """
    entries = os.listdir(str(path))
    if all is None and almost_all is None:
        entries = [f for f in entries if f[0] != '.']
    if all:
        entries += ['.', '..']
    if ignore_backups:
        entries = [e for e in entries if e[-1] != '~']
    return entries

# !!! Add SELinux context
# !!! add mode argument
def mkdir(*paths,**kw):
    """
    Python translation of GNU mkdir.

    Make the directories passed as *PATHS.
    If PARENTS is truthy, make parent directories as needed.

    Arguments:
    - `paths`: str or Path
    - `parents`: bool

    Return: None
    Exceptions: None
    """
    fn = 'parents' in kw and kw['parents'] and mkdir_p or os.mkdir
    for path in paths:
        try:
            fn(str(path))
        except OSError as err:
            if err.errno == 2:
                msg = 'Target {0} lacked some parents'.format(path)
                raise exceptions.BadParentingError(msg)
            raise
    return

def mkdir_p(path):
    """
    Python translation of *nix mkdir -p

    Will create all components in `path` which do not exist.

    Arguments:
    - `path`: str or Path

    Return: None
    Exceptions: Exception
    """
    try:
        os.makedirs(str(path))
    except OSError: # Python > 2.5
        _, exc, _ = sys.exc_info()
        if exc.errno == errno.EEXIST:
            pass
        else: raise

def mv(resource, target):
    """
    Move RESOURCE to TARGET.

    Arguments:
    - `resource`: str
    - `target`: str

    Return: None
    Exceptions:None
    """
    try:
        shutil.move(resource, target)
    except shutil.Error:
        if not os.path.exists(target):
            rm(target, recursive=True)
            shutil.move(resource, target)
            if os.path.exists(resource):
                rm(resource, recursive=True)


def pwd():
    """
    Python port of the *nix pwd command.

    Prints the current working directory
    """
    print(getcwd())
    return

def rm(*targets, **kw):
    """
    Python translation of GNU rm

    If the keyword argument FORCE is True, ignore nonexistant files.
    If the keyword argument RECURSIVE is True, remove the entire tree
      below each TARGETS

    Arguments:
    - `*targets`: all target paths
    - `force`: bool
    - `recursive`: bool

    Return: None
    Exceptions: DoesNotExistError
    """
    fn = os.remove
    if 'recursive'in kw and kw['recursive']:
        fn = rm_r
    if 'force' in kw and kw['force']:
        for target in targets:
            try:
                fn(str(target))
            except OSError:
                pass # Either never raised or explicitly ignored, so pass
    else:
        for target in targets:
            try:
                fn(str(target))
            except OSError:
                if not os.path.exists(str(target)):
                    raise exceptions.DoesNotExistError(
                        "No such file {0} Larry... ".format(target))
                else:
                    raise
    return

# !!! Wrap to accept Path
rm_r = shutil.rmtree

# ::rm_rf (FileUtils)

# !!! Wrap to accept Path
rmdir = os.rmdir

# !!! Wrap to accept Path
stat = os.stat

def touch(fname):
    """
    Python port of the Unix touch command

    Create a file at FNAME if one does not exist

    Arguments:
    - `path`: str or Path

    Return: None
    Exceptions: Exception
    """
    with open(str(fname), 'a'):
        pass
    return

unlink = os.unlink

def which(program):
    """
    Python port of the Unix which command.

    Examine PATH to see if `program' is on it.
    Return either the fully qualified filename or None

    Arguments:
    - `program`: str

    Return: str or None
    Exceptions: None
    """
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None

def is_exe(fpath):
    """
    Is `fpath' executable?

    Arguments:
    - `fpath`: str

    Return: bool
    Exceptions: None
    """
    return os.path.exists(fpath) and os.access(fpath, os.X_OK)

def is_file(path):
    """
    Predicate to determine if PATH is a file

    Arguments:
    - `path`: str or Path

    Return: bool

    Exceptions: None
    """
    return os.path.isfile(str(path))
