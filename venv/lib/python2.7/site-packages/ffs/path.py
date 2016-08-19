"""
ffs.path

Pathname API
"""
from __future__ import with_statement

import contextlib
import fnmatch
import hashlib
try:
    import simplejson as json
except ImportError:
    import json
import mimetypes
import os
import re
import tempfile
import traceback
import types

import six

from ffs import (exceptions, filesystem, formats, nix, is_dir, is_file, size,
                 _path_blacklists)

def _stringcoll(coll):
    """
    Predicate function to determine whether COLL is a non-empty
    collection (list/tuple) containing only strings.

    Arguments:
    - `coll`:*

    Return: bool
    Exceptions: None
    """
    if isinstance(coll, (list, tuple)) and coll:
        return len([s for s in coll if isinstance(s, six.string_types)]) == len(coll)
    return False

class Pset(set):
    """
    Set subclass for representing collections of paths
    """

    @property
    def basenames(self):
        """
        Return the basenames for our path collection

        Return: iterable
        Exceptions: None
        """
        return Pset(p[-1] for p in self)


# !!! Normalization to clean up ../, . && //

class BasePath(str):
    """
    Base Path class from which other implementations will inherit
    """
    fsflavour = filesystem.DiskFilesystem

    def __new__(kls, *args, **kwargs):
        if len(args) > 0 and isinstance(args[0], six.string_types) and args[0].startswith('http://'):
            from ffs.contrib.http import HTTPPath
            if kls != HTTPPath:
                return HTTPPath(args[0])
        return super(BasePath, kls).__new__(kls, *args, **kwargs)

    def __init__(self, value=None):
        """
        as str objects are immutable, we must store the 'value'
        as an instance variable
        """
        self.fs = self.fsflavour()
        if value is None:
            self._value = self.fs.getwd()
        elif isinstance(value, (list, tuple)):
            if not value:
                self._value = ''
            elif not _stringcoll(value):
                raise TypeError('can only accept collections of strings larry')
            self._value = self.fs.sep.join(value)
        elif isinstance(value, Path):
            self._value = value._value
        elif isinstance(value, six.string_types):
            self._value = value
        else:
            raise TypeError("don't know how to initialize with {0} larry... ".format(value))
        # these are used by contextmanagers possibly
        self._file = None
        self._startdir = None
        self._readlinegen = None
        return

    def __repr__(self):
        return self

    def __str__(self):
        return self._value

    def __unicode__(self):
        return unicode(str(self))

    def __eq__(self, other):
        """
        custom equality tests.

        if the other is a string, compare against our self._value.
        if the other is a path, likewise.
        if the other is anything else, say no.
        """
        if isinstance(other, six.string_types):
            return self._value == other
        return False

    def __hash__(self):
        """
        we take the hashed value as that of the str _value.
        this is to allow the idiom:
        >>> p = path('/foo')
        >>> d = dict(p=1)
        >>> assert d['/foo'] == 1

        return: int
        exceptions: none
        """
        return hash(self._value)

    def __nonzero__(self):
        """
        determine whether this is a path on the current filesystem.

        allows the idiom:

        >>> if self:
        ...     with self as fh:
        ...         print self.read()

        return: bool
        exceptions:
        """
        return self.fs.exists(self._value)

    # Py3k compatibility
    __bool__ = __nonzero__

    def __len__(self):
        """
        determine the length of our path

        return: int
        exceptions: none
        """
        return len(self._split)

    def __getattribute__(self, attr):
        """
        we override getattribute largely to allow us to blacklist
        string methods that are not appropriate for path objects,
        despite inheriting from str for stdlib duck-typing purposes.
        """
        if attr in _path_blacklists._strblacklist:
            msg = "'path' object has no attribute '{0}'".format(attr)
            raise AttributeError(msg)

        return super(str, self).__getattribute__(attr)

    def __getitem__(self, key):
        """
        return the path component at key

        arguments:
        - `slicenum`: int

        return: path
        exceptions: indexerror
        """
        Klass = self.__class__
        # delegate to the list implementation
        # we're relying on this to raise the correct exceptions
        interesting = self._split.__getitem__(key)

        # if a single element, return just that
        if isinstance(key, int):
            return Klass(interesting)

        # if we asked for [:int] and we're an abspath, prepend it
        if isinstance(key, slice):
            if key.start in [None, 0] and key.stop:
                # !!! what does joining by '/' do on windoze?
                frist = '{0}{1}'.format(self.fs.sep if self.is_abspath else '', interesting[0])
                interesting[0] = frist

        return Klass(self.fs.sep.join(interesting))

    def __getslice__(self, *args):
        """
        as we're subclassing string, we have to override getslice.
        this is a backwards compatibility hack, we just delegate to the
        more modern getitem.

        Unless we're being called from os.path on a posix platform.
        In which case we should pretend to be a string.
        """
        stack = traceback.extract_stack()
        fname, line, fn, code = stack[-2]
        if fname.find('posixpath') != -1 and fn == 'split':
            return str(self).__getitem__(slice(*args))
        return self.__getitem__(slice(*args))

    def __setitem__(self, key, value):
        """
        paths are immutable, so raise TypeError

        arguments:
        - `key`: object
        - `value`: object

        return: None
        exceptions: TypeError
        """
        raise TypeError('path object does not support item assignment')

    # !!! todo: do we want to do disk access here?
    # !!! this behaves differently to __iter__.
    def __contains__(self, item):
        """
        determine if item is in the path

        arguments:
        - `item`: str

        return: bool
        exceptions: None
        """
        if item == '?':
            return item in self._value
        if item[0] == self.fs.sep:
            regexp = r'^{0}'.format(item)
        else:
            regexp = r'^{0}|(?<=/){0}'.format(item)
        if re.search(regexp, self._value):
            return True
        return False

    def __add__(self, other):
        """
        add something to ourself, returning a new path object.

        if other is a path or a string, append other to self.
        if other is an empty collection, do nothing.
        if other is a collection containing items that are not strings, raise TypeError
        if other is a collection containing strings, append each to self as a
           path component.
        otherwise, raise TypeError

        arguments:
        - `other`:*

        return: path
        exceptions: TypeError
        """
        klass = self.__class__
        # path()s and strings are simple
        if isinstance(other, Path):
            return self + other._value
        if isinstance(other, six.string_types):
            return klass(self.fs.sep.join([self._value, other]))

        # collections must be typechecked. weak runtime type safety, yes, i know.
        if isinstance(other, (list, tuple)):
            if not other:
                return self
            if not _stringcoll(other):
                raise TypeError('can only add collections containing string types')
            return self + self.fs.sep.join(other)

        raise TypeError()

    # !!! accept path() and collections
    def __iadd__(self, other):
        """
        in place addition overloading.

        we want to include the path separator
        """
        Klass = self.__class__
        if not isinstance(other, six.string_types):
            raise TypeError
        # !!! what should we do on windoze?
        if other[0] == self.fs.sep:
            return Klass('{0}{1}'.format(self, other))
        return Klass('{0}{1}{2}'.format(self, self.fs.sep, other))

    # !!! deal with different path.sep
    def __radd__(self, other):
        """
        add to the right of a string

        we want to include the path separator
        """
        Klass = self.__class__
        if not isinstance(other, six.string_types):
            raise TypeError
        # !!! what should this do on windoze?
        if other[0] == self.fs.sep:
            frist = self.fs.sep
        else:
            frist = ''
        branches = [b for b in other.split(self.fs.sep) + self._split if b]
        return Klass('{0}{1}'.format(frist, self.fs.sep.join(branches)))

    def __div__(self, other):
        """
        we overload the division operator to be path addition.

        if other is not a str or path, we raise TypeError.

        arguments:
        - `other`: str or path

        return: path
        exceptions: TypeError
        """
        return self + other

    def __truediv__(self, other):
        """
        Overload all the division operators
        """
        return self + other

    @property
    def is_abspath(self):
        """
        Predicate property to determine if this is an absolute path

        Return: bool
        Exceptions: None
        """
        # !!! Windoze?
        return self._value[0] == self.fs.sep

    @property
    def _split(self):
        """
        Split the value ignoring the leading / if it exists

        Return: list<str>
        Exceptions: None
        """
        if self.is_abspath:
            return self._value[1:].split(self.fs.sep)
        return self._value.split(self.fs.sep)

    @property
    def abspath(self):
        """
        Return the absolute path represented by SELF.

        If SELF begins with a /, assume a fully qualified name.
        If not and the ~ construction is in SELF, expand it.

        Return: Path
        Exceptions: None
        """
        if self.is_abspath:
            return self
        return Path(self.fs.abspath(self))

    @property
    def parent(self):
        """
        Return a Path object representing the parent of SELF

        Return: Path
        Exceptions: None
        """
        strself = str(self)
        parnt = self.fs.parent(strself)
        return Path(parnt)

    # !!! ext

    # !!! Split - change default arg

    def ls(self, *args, **kwargs):
        """
        If we are a directory, return an iterable of the contents.

        If we are a file, return the name.

        If we don't exist, raise DoesNotExistError.

        If we have passed PATTERN, then only return such entries as match

        Arguments:
        - `pattern`: str

        Return: iterable or string
        Exceptions: DoesNotExistError
        """
        if self.is_file:
            return self._value
        elif self.is_dir:
            all = kwargs.get('all', None)
            contents =  self.fs.ls(self, all=all)
            if args:
                contents = fnmatch.filter(contents, args[0])
            if len(contents) == 0:
                return []
            return Pset(self/x for x in contents)

        msg = "Cannot access {0}: No such file or directory".format(self)
        raise exceptions.DoesNotExistError(msg)

    # !!! json_dump()
    # !!! pickle_load()
    # !!! pickle_dump()

class LeafBranchPath(BasePath):

    @property
    def is_dir(self):
        """
        Predicate property to determine if this is an existng directory

        Return: bool
        Exceptions: None
        """
        return self.fs.is_branch(self._value)

    @property
    def is_file(self):
        """
        Predicate property to determine if this is an existng file

        Return: bool
        Exceptions: None
        """
        return self.fs.is_leaf(self._value)

    @contextlib.contextmanager
    def open(self, mode):
        """
        Contextmanager to open SELF in the mode specified.

        If SELF is a directory, raise TypeError

        Note::

            If components of the path leading to SELF do not exist,
            they will be created. It is assumed that the user knows their
            own mind.

        Arguments:
        - `mode`: str

        Return: file
        Exceptions: TypeError
        """
        if self.is_dir:
            raise TypeError("Opening a directory doesn't really mean anything Larry... ")
        if not self.fs.is_branch(self.parent): # we only have to check one level
            self.fs.mkdir((self[:-1]), parents=True)
        with self.fs.open(self._value, mode) as fh:
            yield fh

    def read(self):
        """
        Read the contents of the file SELF.

        Allows us to duck-type as a file.

        If SELF is a directory, raise TypeError.

        Return: str
        Exceptions: TypeError
        """
        if self.is_dir:
            raise TypeError("Reading a directory doesn't make any sense Larry... ")
        with self.open('r') as fh:
            return fh.read()

    def readline(self):
        """
        Duck-typing like a file.

        Read one entire line from the file. A trailing newline character is kept in the string.

        If SELF is a directory or does not exist, raise TypeError.

        Return: str
        Exceptions: TypeError
        """
        if not self:
            raise TypeError("Can't read something that doesn't exist Larry... ")
        if self.is_dir:
            raise TypeError("Can't read a directory Larry... ")
        if not self._readlinegen:
            self._readlinegen = self.__iter__()
        try:
            return six.next(self._readlinegen)
        except StopIteration:
            return ""

    def truncate(self):
        """
        Duck-typing like a file

        Truncate the file's size.

        If SELF is a directory or does not exist, raise TypeError

        Return: None
        Exceptions: TypeError
        """
        if not self:
            raise TypeError("Can't truncate something that doesn't exist Larry... ")
        if self.is_dir:
            raise TypeError("Can't truncate a directory Larry... ")
        with self.open('w') as fh:
            fh.truncate()
        return

    @property
    def contents(self):
        """
        The contents of SELF.

        If SELF is a file, read the contents.
        If SELF is a directory, alias of ls()

        Return: str or list[str]
        Exceptions: None
        """
        if self.is_dir:
            return self.ls()
        elif self.is_file:
            return self.read()
        msg = "{0} isn't a thing Larry - how can it have contents?"
        raise exceptions.DoesNotExistError(msg)

    @property
    def as_zip(self):
        """
        Attempt to return the current path as a .zip path.

        For the possible errors this can raise, see contrib.archive.ZipPath
        """
        from ffs.contrib.archive import ZipPath
        return ZipPath(self, error_if_not_found=True)

    def json_load(self):
        """
        Treat SELF as a file containing JSON serialized data.
        Load that data and return it.

        If SELF is a directory or does not exist, raise TypeError

        Return: object
        Exceptions: TypeError
        """
        if not self:
            raise TypeError("Can't load something that doesn't exist Larry... ")
        if self.is_dir:
            raise TypeError("Can't tread a directory as JSON Larry... ")
        return json.loads(self.contents)
    

class Path(LeafBranchPath):
    """
    Provide a pleasant API for working with file/directory paths.

    If VALUE is None, then then initial value is the current working directory.
    If VALUE is a string, take this to be a filesystem path of some description.
    If VALUE is a list or tuple containing strings, take these as components of a
      filesytem path.
    If VALUE is a list or tuple containing non-strings, non-Paths, raise TypeError.

    Arguments:
    - `value`: str or list[str]

    Return: None
    Exceptions: TypeError
    """

    # !! this behaves differently to __contains__
    def __iter__(self):
        """
        path objects iterate differently depending on context.

        if we are a directory, we iterate through path objects
        representing the contents of that directory.

        if we represent a file, iteration returns one line at a time.

        if we do not exist, we raise DoesNotExistError

        return: generator(str or path)
        exceptions: DoesNotExistError
        """
        if self.is_dir:

            def dirgen():
                "directory list generator"
                for k in self.fs.ls(self._value):
                    yield Path(k)
            return dirgen()

        elif self.is_file:
            def filegen():
                "file generator"
                with self as fh:
                    for line in fh:
                        yield line

            return filegen()

        msg = 'the path {0} does not exist - not sure how to iterate'.format(self)
        raise exceptions.DoesNotExistError(msg)

    def __lshift__(self, contents):
        """
        we overload the << operator to allow us easy file writing according to the
        following rules:

        if we are a directory, raise TypeError.
        if contents is not a stringtype, raise TypeError.

        otherwise, treat self like a file and append contents to it.

        note::

            if components of the path leading to self do not exist,
            they will be created. it is assumed that the user knows their
            own mind.

        arguments:
        - `contents`: stringtype

        return: None
        exceptions: TypeError
        """
        if self.is_dir:
            raise TypeError("you can't write to a directory Larry... ")
        if not isinstance(contents, six.string_types):
            raise TypeError("you have to write with a stringtype Larry... ")
        with self.open('a') as fh:
            fh.write(contents)
        return

    def __enter__(self):
        """
        contextmanager code - if the path is a file, this should behave like
        with open(path) as foo:

        if this is a directory, it should cd there and then return
        """
        if self.is_file:
            self._file = self.fs.open(self._value)
            return self._file
        elif self.is_dir:
            self._startdir = self.fs.getwd()
            self.fs.cd(self)
            return

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Contextmanager handling.
        Exit from opening the path
        """
        if self.is_file:
            try:
                self._file.close()
            finally:
                self._file = None
        elif self.is_dir:
            self.fs.cd(self._startdir)
            self._startdir = None
        return

    @property
    def size(self):
        """
        Return the size of SELF in bytes

        Return: int
        Exceptions: DoesNotExistError
        """
        return size(self)

    @classmethod
    @contextlib.contextmanager
    def temp(klass):
        """
        Create a temporary path within a contextmanager block
        which will be automatically deleted when we exit the block

        Return: Path
        Exceptions: None
        """
        fs = klass.fsflavour()
        tmpath = fs.tempdir()
        try:
            yield klass(tmpath)
        finally:
            fs.rm(tmpath, recursive=True)

    @classmethod
    @contextlib.contextmanager
    def tempfile(klass):
        """
        Create a temporary file.

        If this is called as a contextmanager, delete
        the file on exiting the block, else leave it to the
        user to delete as appropriate.

        Return: Path
        Exceptions: None
        """
        fs = klass.fsflavour()
        tmpath = fs.tempfile()
        pth = klass(tmpath)
        pth.touch()
        try:
            yield pth
        finally:
            fs.rm(tmpath)
        return

    @classmethod
    def newdir(klass):
        """
        Create a directory that previously did not exist.
        (Typically in the system's temp dir)

        Return: klass()
        Exceptions: None
        """
        fs = klass.fsflavour()
        tmpath = fs.tempdir()
        return klass(tmpath)

    @classmethod
    def newfile(klass, filename=None):
        """
        Create a file that previously did not exist.
        (typically in the system's temp dir)

        Return: klass()
        Exceptions: None
        """
        fs = klass.fsflavour()
        if not filename:
            tmpfile = fs.tempfile()
            pth = klass(tmpfile)
            pth.touch()
            return pth
        else:
            tdir = klass.newdir()
            newpath = tdir/filename
            newpath.touch()
            return newpath
            
    @staticmethod
    def here():
        """
        Return a path representing the directory of the
        file that this method was called from.

        Return: Path
        Exceptions: None
        """
        stack = traceback.extract_stack()
        me = __file__
        if me.endswith('.pyc') or me.endswith('.pyo'):    # Bytecode!
            me = me [:-1]

        for i, frame in enumerate(stack):
            if frame[0] == me:
                there = stack[i-1][0]
                return Path(there).abspath.parent

        return

    def touch(self, *args):
        """
        Equivalent to calling the *nix command touch on SELF.

        Creates a file if one does not exist, otherwise, a no-op.

        If self is a directory, raise TypeError

        If *ARGS is non-null, treat each item in *ARGS as a child node of
        SELF, and touch these files

        Arguments:
        - `*ARGS`: str

        Return: None
        Exceptions: TypeError
        """
        if self.is_dir and not args:
            raise TypeError("Can't touch() a directory!")
        if not args:
            self.fs.touch(self)
        else:
            if not self:
                self.fs.mkdir(self, parents=True)
            for arg in args:
                tfile = self + arg
                if not tfile.parent:
                    self.fs.mkdir(tfile.parent, parents=True)
                self.fs.touch(tfile)

    def mkdir(self, *args):
        """
        Equivalent to calling the *nix command on SELF.

        Creates a directory if one does not exist, otherwise, a no-op.
        Implicitly creates parents if required.

        If self is a file, raise TypeError

        If *ARGS is non-null, treat each item in *ARGS as a child node of
        SELF, and create these directories.

        Arguments:
        - `*ARGS`: str
        - `parents`: bool

        Return: None
        Exceptions: TypeError
        """
        if self.is_file:
            raise TypeError("Can't mkdir() a file.")
        if not args:
            self.fs.mkdir(self, parents=True)
        else:
            for arg in args:
                self.fs.mkdir(self + arg, parents=True)
        return

    def cp(self, target):
        """
        Copy SELF to TARGET.

        If SELF is a directory, assume that you want to copy the tree.
        If SELF does not exist, raise DoesNotExistError.

        Arguments:
        - `target`: str or Path

        Return: None
        Exceptions: DoesNotExistError
        """
        recursive = False
        if self.is_dir:
            recursive = True
        self.fs.cp(self, target, recursive=recursive)
        return

    def mv(self, target):
        """
        Move SELF to TARGET.
        Return a Path object representing the new location at TARGET.

        If SELF does not exist, raise DoesNotExistError

        Arguments:
        - `target`: str or Path

        Return: Path
        Exceptions: DoesNotExistError
        """
        if not self:
            raise exceptions.DoesNotExistError("Can't move nothing Larry... ")
        self.fs.mv(self, target)
        return Path(target)

    #!!! Implement this
    def rm(self,* patterns):
        """
        If PATTERNS is empty, remove SELF.

        Otherwise PATTERNS should be n items to remove.
        PATTERNS themselves can contain glob patterns, and all matching
        pathnames will be removed.

        Arguments:
        - `*patterns`: str

        Return: None
        Exceptions: None
        """
        self.fs.rm(self)

    @contextlib.contextmanager
    def csv(self, delimiter=',', header=False):
        """
        Contextmanager to use SELF as a csv.Reader object

        Use DELIMITER as the csv's delimiter

        If HEADER is True, consume the frist row of the CSV as a header,
        and use this to generate a namedtuple from the CSV.
        Return rows as instances of this namedtuple.

        Arguments:
        - `delimiter`: str
        - `header`: bool

        Return: csv.Reader
        Exceptions: None
        """
        with formats.CSV(self, delimiter=delimiter, header=header) as csv:
            yield csv

    @property
    def mimetype(self):
        """
        Return a guessed mimetype for SELF.

        If SELF is a directory, raise InappropriateError
        If SELF is nonexistant, raise DoesNotExistError

        Return: str
        Exceptions: InappropriateError, DoesNotExistError
        """
        if not self:
            raise exceptions.DoesNotExistError()
        if self.is_dir:
            raise exceptions.InappropriateError()
        mime, _ = mimetypes.guess_type(str(self))
        return mime

    @property
    def checksum(self):
        """
        Return an MD5 checksum of this file. 

        If SELF is a directory, raise InappropriateError
        If SELF is nonexistant, raise DoesNotExistError

        Return: str
        """
        if not self:
            raise exceptions.DoesNotExistError()
        if self.is_dir:
            raise exceptions.InappropriateError()
        checksum = hashlib.md5(self.open('rb').read()).hexdigest()
        return checksum
        
    # !!! json_dump()
    # !!! pickle_load()
    # !!! pickle_dump()
