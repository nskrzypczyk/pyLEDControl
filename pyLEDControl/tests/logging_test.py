from misc.logging import Log
import unittest

class LoggingTests(unittest.TestCase):
    def setUp(self):
        self.log = Log(__name__,"DEBUG")

