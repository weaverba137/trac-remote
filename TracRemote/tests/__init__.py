# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""
================
TracRemote.tests
================

Contains initialization for the unit test framework via ``python setup.py test``.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import unittest
from os.path import dirname


def TracRemote_test_suite():
    """Returns unittest.TestSuite of TracRemote tests.
    """
    TracRemote_dir = dirname(dirname(__file__))
    tl = dirname(TracRemote_dir)
    # print(TracRemote_dir)
    return unittest.defaultTestLoader.discover(TracRemote_dir,
                                               top_level_dir=tl)


def runtests():
    """Run all tests in TracRemote.tests.test_*.
    """
    # Load all TestCase classes from TracRemote/tests/test_*.py
    tests = TracRemote_test_suite()
    # Run them
    unittest.TextTestRunner(verbosity=2).run(tests)
