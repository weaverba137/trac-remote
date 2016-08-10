# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""
==========================
TracRemote.tests.test_main
==========================

Test functions and classes in the main module.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import unittest
# from pkg_resources import resource_filename
from ..main import main_args


class TestMain(unittest.TestCase):
    """Test functions and classes in the main module.
    """

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_main_args(self):
        """Test the argument-parsing function.
        """
        options = main_args(['http://www.example.com', 'wiki', 'list'])
        self.assertEqual(options.URL, 'http://www.example.com')
        self.assertEqual(options.cmd_name, 'wiki')
        self.assertEqual(options.command, 'list')
