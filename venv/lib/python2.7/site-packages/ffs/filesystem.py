"""
ffs.filesystem

Filesystem abstraction to allow working with different
filesystem-like systems with the same abstraction model.
"""
from __future__ import with_statement

import os
import tempfile

from ffs import exceptions, nix, util
from ffs.util import wraps

class BaseFilesystem(object):
    """
    The base class from which all filesystem implementations
    inherit.

    This class is used to establish the interface, as well as provide
    some generic helper methods.
    """

    def exists(self, resource):
        """
        Predicate function to determine whether RESOURCE exists.

        Arguments:
        - `resource`: str or Path

        Return: bool
        Exceptions: None
        """
        raise NotImplementedError('!')

    @property
    def sep(self):
        """
        The node separator used by this filesystem
        """
        raise NotImplementedError('!')

    def getwd(self):
        """
        Should return the 'current working directory' for this
        filesystem.

        Return: str
        Exceptions: None
        """
        raise NotImplementedError("!")

    def ls(self, branch):
        """
        Return a list of the contents of BRANCH

        Arguments:
        - `branch`: str or Path

        Return: [str or Path]
        Exceptions: None
        """
        raise NotImplementedError("!")

    def cd(self, target):
        """
        Change the working directory to TARGET

        The return is a contextmanager, for which __enter__ is a
        no-op - the work is done in the constructor. This means that
        cd() can be used both as a function and as a contextmanager

        >>> fs.cd('/tmp')
        >>> fs.getwd()
        /tmp
        >>> with fs.cd('/'):
        ...     print fs.getwd()
        ...
        /
        >>> fs.getwd()
        /tmp

        Arguments:
        - `target`: str or Path

        Return: Contextmanager
        Exceptions: None
        """
        raise NotImplementedError("!")

    def is_abspath(self, path):
        """
        Is PATH a representation of an absolute path on this
        filesystem?

        Arguments:
        - `path`: str or Path

        Return: bool
        Exceptions: None
        """
        raise NotImplementedError("!")

    def open(self, resource, mode='r'):
        """
        Open RESOURCE as a file-like object

        Arguments:
        - `resource`: str or Path
        - `mode`: str

        Return: File-like-object
        Exceptions: None
        """
        raise NotImplementedError("!")

    def is_branch(self, resource):
        """
        Is RESOURCE a branch node on this filesystem?

        Arguments:
        - `resource`: str or Path

        Return: bool
        Exceptions: None
        """
        raise NotImplementedError("!")

    def is_leaf(self, resource):
        """
        Is RESOURCE a leaf node on this filesystem?

        Arguments:
        - `resource`: str or Path

        Return: bool
        Exceptions: None
        """
        raise NotImplementedError("!")

    def expanduser(self, resource):
        """
        Expand ~ etc for RESOURCE

        Arguments:
        - `resource`: str or Path

        Return: str or Path
        Exceptions: None
        """
        raise NotImplementedError("!")

    def abspath(self, resource):
        """
        Return the absolute path for RESOURCE given the
        current state of our filesystem representation.

        Implicitly calls expanduser on RESOURCE.

        Arguments:
        - `resource`: str or Path

        Return: str or Path
        Exceptions: None
        """
        raise NotImplementedError("!")

    def parent(self, resource):
        """
        Return the parent branch of RESOURCE

        Arguments:
        - `resource`: str or Path

        Return: str or Path
        Exceptions: None
        """
        raise NotImplementedError("!")

    def mkdir(self, path, parents=False):
        """
        Create the branch PATH on our filesystem.

        If PARENTS is truthy, make parent directories as needed.

        Arguments:
        - `path`: str or Path

        Return: None
        Exceptions: None
        """
        raise NotImplementedError("!")

    def cp(self, resource, target, recursive=False):
        """
        Copy RESOURCE to TARGET.
        If RECURSIVE is True, copy the tree below RESOURCE recursively.

        Arguments:
        - `resource`: str or Path
        - `target`: str or Path
        - `recursive`: bool

        Return: None
        Exceptions: None
        """
        raise NotImplementedError("!")

    def ln(self, resource, target, symbolic=False):
        """
        Link RESOURCE to TARGET.

        If SYMBOLIC is True, create a symlink.

        Arguments:
        - `resource`: str or Path
        - `target`: str or Path

        Return: None
        Exceptions: None
        """
        raise NotImplementedError("!")

    def mv(self, resource, target):
        """
        Move RESOURCE to TARGET.

        Arguments:
        - `resource`: str or Path
        - `target`: str or Path


        Return:  None
        Exceptions: None
        """
        raise NotImplementedError("!")

    def touch(self, resource):
        """
        Create a leaf node RESOURCE on the filesystem

        Arguments:
        - `resource`: str or Path

        Return: None
        Exceptions: None
        """
        raise NotImplementedError("!")

    def tempfile(self):
        """
        Create a temporary file on this filesystem.

        Return: str or Path
        Exceptions: None
        """
        raise NotImplementedError("!")

    def tempdir(self):
        """
        Create a temporary directory on this filesystem and return it's path.

        Return: str or Path
        Exceptions: None
        """
        raise NotImplementedError("!")

    def stat(self, resource):
        """
        Return stat info (or equivalent) about RESOUCE

        Arguments:
        - `resource`: str or Path

        Return: namedtuple
        Exceptions: None
        """
        raise NotImplementedError("!")

    def rm(self, resource, recursive=False):
        """
        Remove RESOURCE from the filesystem

        If the keyword argument RECURSIVE is True, remove the tree below
          this point.

        Arguments:
        - `resource`: str or Path
        - `recursive`: bool

        Return: None
        Exceptions: None
        """
        raise NotImplementedError("!")


class ReadOnlyFilesystem(BaseFilesystem):
    """
    A filesystem that only allows us read access to it's contents.

    We explicitly stop raising NotImplementedError so that subclasses won't
    have to. Instead, we raise InappropriateError. Pedantic, but more semantic.
    """

    def mkdir(self, resource):
        raise exceptions.InappropriateError("Can't mkdir() on a Read-only filesystem")

    def cp(self, resource, target):
        raise exceptions.InappropriateError("Can't cp() on a Read-only filesystem")

    def ln(self, resource, target):
        raise exceptions.InappropriateError("Can't ln() on a Read-only filesystem")

    def mv(self, resource, target):
        raise exceptions.InappropriateError("Can't mv() on a Read-only filesystem")

    def rm(self, resource):
        raise exceptions.InappropriateError("Can't rm() on a Read-only filesystem")

    def touch(self, resource):
        raise exceptions.InappropriateError("Can't touch() on a Read-only filesystem")

    def tempfile(self):
        raise exceptions.InappropriateError("Can't tempfile() on a Read-only filesystem")

    def tempdir(self):
        raise exceptions.InappropriateError("Can't tempdir() on a Read-only filesystem")


class DiskFilesystem(BaseFilesystem):
    """
    Disk based filesystem. Abstraction across implementations
    handled by Python standard library.
    """

    @property
    @wraps(BaseFilesystem.sep)
    def sep(self):
        return os.sep

    @wraps(BaseFilesystem.exists)
    def exists(self, resource):
        return os.path.exists(resource)

    @wraps(BaseFilesystem.getwd)
    def getwd(self):
        return nix.getwd()

    @wraps(BaseFilesystem.ls)
    def ls(self, resource, all=None):
        return nix.ls(resource, all=all)

    @wraps(BaseFilesystem.cd)
    def cd(self, target):
        return nix.cd(target)

    @wraps(BaseFilesystem.is_abspath)
    def is_abspath(self, resource):
        return resource[0] == self.sep

    @wraps(BaseFilesystem.is_branch)
    def is_branch(self, resource):
        return util.is_dir(resource)

    @wraps(BaseFilesystem.is_leaf)
    def is_leaf(self, resource):
        return util.is_file(resource)

    @wraps(BaseFilesystem.parent)
    def parent(self, resource):
        return os.path.dirname(resource)

    @wraps(BaseFilesystem.open)
    def open(self, resource, mode='r'):
        return open(self.expanduser(resource), mode)

    @wraps(BaseFilesystem.expanduser)
    def expanduser(self, resource):
        return os.path.expanduser(resource)

    @wraps(BaseFilesystem.abspath)
    def abspath(self, resource):
        return os.path.abspath(self.expanduser(resource))

    @wraps(BaseFilesystem.mkdir)
    def mkdir(self, resource, parents=False):
        return nix.mkdir(resource, parents=parents)

    @wraps(BaseFilesystem.cp)
    def cp(self, resource, target, recursive=False):
        return nix.cp(resource, target, recursive=recursive)

    @wraps(BaseFilesystem.ln)
    def ln(self, resource, target, symbolic=False):
        return nix.ln(resource, target, symbolic=symbolic)

    @wraps(BaseFilesystem.mv)
    def mv(self, resource, target):
        return nix.mv(resource, target)

    @wraps(BaseFilesystem.touch)
    def touch(self, resource):
        return nix.touch(resource)

    @wraps(BaseFilesystem.tempfile)
    def tempfile(self):
        tfile = tempfile.mktemp()
        self.touch(tfile)
        return tfile

    @wraps(BaseFilesystem.tempdir)
    def tempdir(self):
        tdir = tempfile.mkdtemp()
        return tdir

    @wraps(BaseFilesystem.rm)
    def rm(self, resource, recursive=False):
        return nix.rm(resource, recursive=recursive)
