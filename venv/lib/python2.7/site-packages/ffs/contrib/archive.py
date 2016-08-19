"""
Ffs implementations of archive formats - treating zip/tar etc as if
they were untarred, transparently.
"""
import tarfile
import zipfile

import six

from ffs import exceptions, nix, path
from ffs.filesystem import BaseFilesystem

class TarFilesystem(BaseFilesystem):
    """
    Tar archive based filesystem.
    """
    sep = '/'

    def __init__(self, archive_path):
        """
        Get ourself a handle to the archive, or raise NotATarFileError
        """
        if not tarfile.is_tarfile(str(archive_path)):
            raise exceptions.NotATarFileError(
                '{0} is not a Tar file Larry :('.format(archive_path))
        self.archive_path = archive_path
        self.tarfile = tarfile.open(archive_path)

    def _get_membernames(self):
        """
        Helper function to find the names of members in our
        tarfile.

        Return:
        Exceptions:
        """
        return self.tarfile.getnames()

    def exists(self, resource):
        """
        Predicate function to determine whether RESOURCE exists.

        Arguments:
        - `resource`: str or Path

        Return: bool
        Exceptions: None
        """
        return resource in self._get_membernames()

    def ls(self, branch):
        """
        Return a list of the contents of BRANCH

        Arguments:
        - `branch`: str or Path

        Return: [str or Path]
        Exceptions: None
        """
        members = self._get_membernames()
        if not branch:
            relevant_members = [m.split(self.sep)[0]
                                for m in members
                                if m.startswith(branch)]
        else:
            relevant_members = [m[len(branch)+1:].split(self.sep)[0]
                                for m in members
                                if m.startswith(branch)]
        return relevant_members

    def open(self, resource, mode='r'):
        """
        Open RESOURCE as a file-like object

        Arguments:
        - `resource`: str or Path

        Return: File-like-object
        Exceptions: None
        """
        return self.tarfile.extractfile(resource)

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

    def mv(self, resource, target):
        """
        Move RESOURCE to TARGET.

        Arguments:
        - resource`: str or Path
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

    def stat(self, resource):
        """
        Return stat info (or equivalent) about RESOUCE

        Arguments:
        - `resource`: str or Path

        Return: TarInfo
        Exceptions: None
        """
        return self.tarfile.getmember(resource)

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
        if not self.exists(resource):
            return False
        item = self.stat(resource)
        if item.isfile():
            return True
        return False

    def ln(self, resource, target, symbolic=False):
        raise exceptions.InappropriateError("Can't ln() on an Archive filesystem")

    def tempfile(self):
        raise exceptions.InappropriateError("Can't ln() on an Archive filesystem")

    def tempdir(self):
        raise exceptions.InappropriateError("Can't ln() on an Archive filesystem")

    def is_abspath(self, path):
        raise exceptions.InappropriateError("Can't is_abspath() on an Archive filesystem")

    def expanduser(self, resource):
        raise exceptions.InappropriateError("Can't expanduser() on an Archive filesystem")

    def abspath(self, resource):
        raise exceptions.InappropriateError("Can't is_abspath() on an Archive filesystem")

    def getwd(self):
        raise exceptions.InappropriateError("Can't getwd() on an Archive filesystem")

    def cd(self, target):
        raise exceptions.InappropriateError("Can't cd() on an Archive filesystem")


class ZipFilesystem(BaseFilesystem):
    """
    Zip archive based filesystem.
    """
    sep = '/'

    def __init__(self, archive_path):
        """
        Get ourself a handle to the archive, or raise NotAZipFileError
        """
        if not zipfile.is_zipfile(str(archive_path)):
            raise exceptions.NotAZipFileError(
                '{0} is not a Zip file Larry :('.format(archive_path))
        self.archive_path = archive_path
        self.zipfile = zipfile.ZipFile(archive_path)


class ZipPath(path.LeafBranchPath):
    """
    Top level entrypoint for working with Zipfiles ffs.
    """
    fsflavour = ZipFilesystem
    
    def __init__(self, archive_path):
        """
        Create our filesystem, store value.
        """
        try:
            self.fs = self.fsflavour(archive_path)
        except exceptions.NotAZipFileError:
            with zipfile.ZipFile(archive_path, 'a') as z:
                z.writestr('.ffs', 'Created by ffs Python')
            self.fs = self.fsflavour(archive_path)
        self._value = archive_path

    def __add__(self, other):
        """
        Add something to ourself, returning a new path object.

        arguments:
        - `other`: *

        return: path
        """
        return ZipContentsPath((self._value, other))

    def __lshift__(self, contents):
        """
        we overload the << operator to allow us easy file writing according to the
        following rules:

        if contents is a tuple of strings, treat the first string as
        the path of the archive contents, and the second as the file
        content.

        otherwise, raise TypeError.

        note::

            if components of the path leading to self do not exist,
            they will be created. it is assumed that the user knows their
            own mind.

        arguments:
        - `contents`: stringtype

        return: None
        exceptions: TypeError
        """
        if not isinstance(contents, tuple):
            raise TypeError("You have to write with tuples Larry...")
        self/contents[0] << contents[1]
        return

    def extract(self, target):
        """
        Extract the Zip archive SELF to TARGET.
        """
        self.fs.zipfile.extractall(target)
        return


class ZipContentsPath(path.LeafBranchPath):
    """
    Path for the contents of a Zip archive
    """
    fsflavour = ZipFilesystem

    def __init__(self, *args):
        """
        Create our filesystem
        """
        archive_path, content = args[0]
        try:
            self.fs = self.fsflavour(archive_path)
        except exceptions.NotAZipFileError:
            with zipfile.ZipFile(archive_path, 'a') as z:
                z.writestr('.ffs', 'Created by ffs Python')
            self.fs = self.fsflavour(archive_path)
        self._archive = archive_path
        self._inner_value = content
        self._value = self.fs.sep.join([archive_path, content])

        
    def __lshift__(self, contents):
        """
        we overload the << operator to allow us easy file writing according to the
        following rules:

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
        if not isinstance(contents, six.string_types):
            raise TypeError("you have to write with a stringtype larry... ")
        temp = path.Path.newdir()
        FOUND = False

        with zipfile.ZipFile(self._archive, 'r') as rz:
            with zipfile.ZipFile(temp/'tmp.zip', 'w') as wz:
                for info in rz.infolist():
                    content = rz.open(info).read()
                    if info.filename == self._inner_value:
                        FOUND = True
                        content += "\n"+contents
                    wz.writestr(info, content)
                if not FOUND:
                    wz.writestr(self._inner_value, contents)
        nix.mv(temp/'tmp.zip', self._archive)
        nix.rmdir(temp)
        return
