"""
Py3k system compatibilities
"""

try:
    FileKlass = file
except NameError:
    from io import TextIOWrapper as FileKlass


