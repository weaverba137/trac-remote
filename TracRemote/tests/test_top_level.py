# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""
===============================
TracRemote.tests.test_top_level
===============================

Test things defined in the top level __init__.py file.
"""
import unittest
import re
from .. import __version__ as tr_version


class TestTop(unittest.TestCase):
    """Test the top-level TracRemote functions.
    """

    @classmethod
    def setUpClass(cls):
        cls.versionre = re.compile(r'''
                                   ([0-9]+!)?  # epoch
                                   ([0-9]+)    # major
                                   (\.[0-9]+)* # minor
                                   ((a|b|rc|\.post|\.dev)[0-9]+)?''',
                                   re.X)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_version(self):
        """Ensure the version conforms to PEP386/PEP440.
        """
        self.assertRegex(tr_version, self.versionre)
