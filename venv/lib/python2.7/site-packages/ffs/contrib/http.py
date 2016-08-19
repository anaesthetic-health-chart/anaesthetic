"""
ffs.contrib.http

An HTTPath implementation on top of ffs.Path.
"""
#
# !!! We should do some further thinking around what constitutes
# an absolute path for http
#
import os
import urlparse

from lxml import html
import requests
import urlhelp

import ffs
from ffs.util import Flike, wraps

class HTTPFlike(Flike):
    """
    A file-like object with a .headers attribute
    """
    def __init__(self, *args, **kw):
        popkw = [
            ('headers', {}),
            ('url', None)
            ]
        for word, default in popkw:
            if word in kw:
                setattr(self, word, kw[word])
                del kw[word]
            else:
                setattr(self, word, default)
        self.dom = html.fromstring(args[0])
        Flike.__init__(self, *args, **kw)

    @property
    def name(self):
        return self.url.split('/')[-1]
        
    def ls(self):
        """
        Return a list of links in this HTML document.

        Return: list[str]
        Exceptions: None
        """
        atags = self.dom.cssselect('a')
        hrefs = [a.attrib['href'] for a in atags]
        hrefs = [h[1:] if h[0] == '/' else h for h in hrefs]
        hrefs = [h if h.startswith('http') else '/'.join([self.url, h]) for h in hrefs ]
        return hrefs


class HTTPFilesystem(ffs.filesystem.ReadOnlyFilesystem):
    """
    An implementation of the ffs filesystem inteface for HTTP.

    We treat this as a Read-only filesystem.
    """
    sep = '/'

    def __init__(self):
        """
        Set up some initial state please.
        """
        self.wd = None

    def expanduser(self, resource):
        """
        On disk filesystems the ~ should expand to a user's HOME.
        Over the internet, this is inappropriate, so raise InappropriateError

        Arguments:
        - `resource`: str or Path

        Exceptions: InappropriateError
        """
        raise ffs.exceptions.InappropriateError("Can't expand users on HTTPPaths Larry... ")

    def exists(self, resource):
        """
        Predicate method to determine whether RESOURCE exists.

        Arguments:
        - `resource`: str or Path

        Return: bool
        Exceptions: None
        """
        resp = requests.head(urlhelp.protocolise(resource))
        return resp.status_code == 200

    def getwd(self):
        """
        Get the current "Working directory".
        For this filesystem metaphor, we stretch it a bit, and take
        http://localhost to be a sensible default.

        If we have previously cd()'d somewhere, we remember that.

        Return: str
        Exceptions: None
        """
        if self.wd:
            return self.wd
        return 'http://localhost'

    def ls(self, resource):
        """
        List the contents of RESOURCE.

        In the contents of an HTTP Filesystem, we take this to mean a
        list of the <a> links on the page.

        Arguments:
        - `resource`: str or Path

        Return: list[str]
        Exceptions: None
        """
        return urlhelp.find_links(resource)

    def cd(self, resource):
        """
        Change our working dir to RESOURCE.

        Can be used as a contextmanager that returns us to whatever
        state we were previously in on exit.

        Arguments:
        - `resource`: str or Path

        Return: None
        Exceptions: None
        """
        oldwd = self.wd
        self.wd = urlhelp.protocolise(resource)

        class HTTPCd(object):
            """
            Define this class in a closure to implement the contextmanager
            protocol while remaining able to operate on SELF.
            """
            def __enter__(zelf):
                return
            def __exit__(zelf, msg, val, tb):
                self.wd = oldwd
                return

        return HTTPCd()

    def is_abspath(self, resource):
        """
        Predicate function to determine whether RESOURCE is an
        absolute path.

        Arguments:
        - `resource`: str or Path

        Return: bool
        Exceptions: None
        """
        if resource == 'localhost':
            return True
        parsed = urlparse.urlparse(resource)
        if parsed.netloc:
            return True
        return False

    def abspath(self, resource):
        """
        Return an absolute path for RESOURCE

        Arguments:
        - `resource`: str or Path

        Return: str
        Exceptions: None
        """
        return urlhelp.protocolise(resource)

    def open(self, resource):
        """
        Return a file-like object that represents the contents of
        a HTTP resource

        Arguments:
        - `resource`: str or Path

        Return: File-Like object
        Exceptions: None
        """
        url = urlhelp.protocolise(resource)
        resp = requests.get(url)
        flike = HTTPFlike(resp.content, url=url, headers=resp.headers)
        return flike

    @wraps(ffs.filesystem.BaseFilesystem.parent)
    def parent(self, resource):
        return os.path.dirname(resource.rstrip(self.sep))

    def is_branch(self, resource):
        """
        For HTTP, we have no canonical way to determine whether RESOURCE
        is a branch or a leaf, so we raise InappropriateError.

        Arguments:
        - `resource`: str or Path

        Exceptions: InappropriateError
        """
        raise ffs.exceptions.InappropriateError("Can't tell if this is a branch Larry... ")

    def is_leaf(self, resource):
        """
        For HTTP, we have no canonical way to determine whether RESOURCE
        is a leaf or a leaf, so we raise InappropriateError.

        Arguments:
        - `resource`: str or Path

        Exceptions: InappropriateError
        """
        raise ffs.exceptions.InappropriateError("Can't tell if this is a leaf Larry... ")


class HTTPPath(ffs.path.BasePath):
    """
    An implementation of the ffs path manupulation interface for
    HTTP resources.
    """
    fsflavour = HTTPFilesystem

    def __init__(self, *args, **kw):
        self._flike = None
        ffs.path.BasePath.__init__(self, *args, **kw)

    def __enter__(self):
        """
        Duck-type a HTTP request like a File.
        Fetch the content, and return it as a File-like-object

        Return: Flike
        Exceptions: None
        """
        # We have to pass the value here because urlparse will
        # iterate through sections, expecting it to be stringy.
        # Which causes Eternal Recursion
        self._flike = self.fs.open(self._value)
        return self._flike

    def __exit__(self, msg, err, tb):
        """
        Clean up the Flike
        """
        try:
            self._flike.close()
        finally:
            self._flike = None

    def __iter__(self):
        """
        Iterate through the lines in the HTTP response content

        Return: iterable
        Exceptions: None
        """
        def httpgen():
            "HTTP Generator"
            with self as fh:
                for line in fh:
                    yield line

        return httpgen()

    # !!! With both this and other addition, figure out a
    # way to do subdomains
    def __iadd__(self, other):
        """
        Implement SELF += str or Path

        Arguments:
        - `other`: str or Path

        Return: HTTPPath
        Exceptions: TypeError
        """
        return ffs.path.BasePath.__iadd__(self, other)

    def open(self):
        """
        Return the content as a file like object
        """
        return self.fs.open(self._value)
