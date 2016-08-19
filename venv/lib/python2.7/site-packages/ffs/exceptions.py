"""
ffs.exceptions

Base and definitions for all exceptions raised by FFS
"""
class Error(Exception):
    "Base Error class for FFS"

class DoesNotExistError(Error):
    "Something should have been here"

class ExistsError(Error):
    "Something already exisis"

class InappropriateError(Error):
    "Someone did something inappropriate"

class NonsenseError(Error):
    "We have encountered a nonsense scenario. Bail."

class NotRaisedError(Error):
    "There is never a good time to raise this"

class BadParentingError(Error):
    "We expected the parents to be there, but no, just a dangling child."

class NotATarFileError(Error):
    "This was supposed to be a tarfile. It is not."

class NotAZipFileError(Error):
    "This was supposed to be a zipfile. It is not."
