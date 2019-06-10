# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""
================================
TracRemote.tests.test_connection
================================

Test the Trac Connection object.
"""
# import unittest
import os
from ..connection import Connection
from .needs_mock import NeedsMock


class TestConnection(NeedsMock):
    """Test the Trac Connection object.
    """

    def test_connection(self):
        """Just test establishing a connection.
        """
        with self.assertRaises(ValueError):
            c = Connection()
        c = Connection(self.url)
        self.assertEqual(c._form_token, 'f5190f99a4efb5b1677f8230')

    def test_password_file(self):
        """Test reading from an arbitrary password file.
        """
        user, password = self.conn._readPassword(self.password_file)
        self.assertEqual(user, 'foo')
        self.assertEqual(password, 'bar')

    def test_index(self):
        """Test the index() method.
        """
        ti = self.conn.index()
        self.assertEqual(ti[1], 'AAAS2016')
        self.assertEqual(ti[-1], 'testRST')

    def test_get(self):
        """Test the get() method.
        """
        text = self.conn.get('TestGet')
        self.assertEqual(text, 'This is a test.\r\n')

    def test_set(self):
        """Test the set() method.
        """
        self.conn.set('TestEdit', 'This is a test.')
        # self.assertEqual(text, 'This is a test.\r\n')

    def test_attachments(self):
        """Test the attachments() method.
        """
        at = self.conn.attachments('TestAttach')
        self.assertIn('carigi.apogge2.lr.utah.pdf', at)
        f = at['carigi.apogge2.lr.utah.pdf']
        self.assertEqual(f['mtime'], '2014-07-29T06:11:13-06:00')
        self.assertEqual(f['size'], 4246601)
        self.assertEqual(f['comment'], 'carigi talk')
        self.assertEqual(f['author'], 'carigi')

    def test_detach(self):
        """Test the detach() method.
        """
        data_file = os.path.join(os.getcwd(), 'password.txt')
        data = self.conn.detach('TestDetach', 'password.txt')
        self.assertEqual(data, 'foo\nbar\n'.encode('utf-8'))
        self.assertTrue(os.path.exists(data_file))
        with open(data_file, 'rb') as d:
            df = d.read()
        self.assertEqual(data, df)
        os.remove(data_file)
        data = self.conn.detach('TestDetach', 'password.txt', save=False)
        self.assertEqual(data, 'foo\nbar\n'.encode('utf-8'))
        self.assertFalse(os.path.exists(data_file))
