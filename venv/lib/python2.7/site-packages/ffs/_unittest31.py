"""
Py3k Unittest assert
"""
from unittest import TestCase as TC, main

class TestCase(TC):
    def assertIsInstance(self, obj, tps):
        self.assertTrue(isinstance(obj, tps))
