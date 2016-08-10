# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""
==========================
TracRemote.tests.test_util
==========================

Test functions and classes in the util module.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import unittest
from pkg_resources import resource_filename
from ..util import (CRLF, SimpleAttachmentHTMLParser, SimpleIndexHTMLParser,
                    SimpleWikiHTMLParser)


class TestUtil(unittest.TestCase):
    """Test functions and classes in the util module.
    """

    @classmethod
    def setUpClass(cls):
        cls.attach = resource_filename('TracRemote.tests', 't/attach.html')
        cls.index = resource_filename('TracRemote.tests', 't/TitleIndex.html')
        cls.login = resource_filename('TracRemote.tests', 't/login.html')
        cls.edit = resource_filename('TracRemote.tests', 't/edit.html')

    @classmethod
    def tearDownClass(cls):
        pass

    def test_CRLF(self):
        """Test the CRLF function.
        """
        text = "\n\n\nThis text\nContains\n\nUnix line-endings\n\n"
        crlf_text = CRLF(text)
        self.assertEqual(crlf_text,
                         ("This text\r\nContains\r\n\r\n" +
                          "Unix line-endings\r\n\r\n"))

    def test_attachment_parser(self):
        """Test attachment list parsing.
        """
        with open(self.attach) as a:
            attach_html = a.read()
        parser = SimpleAttachmentHTMLParser()
        parser.feed(attach_html)
        at = parser.attachments
        self.assertIn('carigi.apogge2.lr.utah.pdf', at)
        f = at['carigi.apogge2.lr.utah.pdf']
        self.assertEqual(f['mtime'], '2014-07-29T06:11:13-06:00')
        self.assertEqual(f['size'], 4246601)
        self.assertEqual(f['comment'], 'carigi talk')

    def test_index_parser(self):
        """Test TitleIndex parsing.
        """
        with open(self.index) as i:
            index_html = i.read()
        parser = SimpleIndexHTMLParser()
        parser.feed(index_html)
        ti = parser.TitleIndex
        self.assertEqual(ti[1], 'AAAS2016')
        self.assertEqual(ti[-1], 'testRST')

    def test_wiki_parser(self):
        """Test wiki parsing.
        """
        with open(self.login) as l:
            login_html = l.read()
        parser = SimpleWikiHTMLParser()
        parser.feed(login_html)
        self.assertEqual(parser.search_value, 'f5190f99a4efb5b1677f8230')
        with open(self.edit) as e:
            edit_html = e.read()
        parser = SimpleWikiHTMLParser('version')
        parser.feed(edit_html)
        self.assertEqual(parser.search_value, '5')
