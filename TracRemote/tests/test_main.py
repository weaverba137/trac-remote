# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""
==========================
TracRemote.tests.test_main
==========================

Test functions and classes in the main module.
"""
# import unittest
# from pkg_resources import resource_filename
from argparse import Namespace
from ..main import main_args, validate_args, dispatch
from .needs_mock import NeedsMock


class TestMain(NeedsMock):
    """Test functions and classes in the main module.
    """

    def test_main_args(self):
        """Test the argument-parsing function.
        """
        options = main_args(['http://www.example.com', 'wiki', 'list'])
        self.assertEqual(options.URL, 'http://www.example.com')
        self.assertEqual(options.cmd_name, 'wiki')
        self.assertEqual(options.command, 'list')
        options = main_args(['http://www.example.com', 'attachment',
                             'list', 'WikiStart'])
        self.assertEqual(options.URL, 'http://www.example.com')
        self.assertEqual(options.cmd_name, 'attachment')
        self.assertEqual(options.command, 'list')
        self.assertEqual(options.arguments[0], 'WikiStart')

    def test_validate_args(self):
        """Test validation of sub-command arguments.
        """
        options = main_args(['http://www.example.com', 'wiki', 'list'])
        self.assertTrue(validate_args(options))
        options = main_args(['http://www.example.com', 'attachment', 'list'])
        self.assertFalse(validate_args(options))

    def test_dispatch(self):
        """Test assignment of commands to connection methods.
        """
        base_options = {'URL': 'http://localhost:8888',
                        'password': None,
                        'realm': None,
                        'debug': False}
        base_options['cmd_name'] = 'wiki'
        base_options['command'] = 'list'
        output = dispatch(Namespace(**base_options))
        self.assertTrue(output.endswith('testRST\n'))
