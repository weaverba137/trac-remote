# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""
==========================
TracRemote.tests.test_util
==========================

Test functions and classes in the util module.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from ..util import CRLF

class TestUtil(unittest.TestCase):

    def test_CRLF(self):
        text = "\n\n\nThis text\nContains\n\nUnix line-endings\n\n"
        crlf_text = CRLF(text)
        self.assertEqual(crlf_text,
                         "This text\r\nContains\r\n\r\nUnix line-endings\r\n\r\n")
