# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""
================================
TracRemote.tests.test_connection
================================

Test the Trac Connection object.
"""
import unittest
import os
import stat
import subprocess
import time
from pkg_resources import resource_filename
from ..connection import Connection


class TestTop(unittest.TestCase):
    """Test the Trac Connection object.
    """

    @classmethod
    def setUpClass(cls):
        cls.url = 'http://localhost:8888'
        cls.netrc_data = """machine localhost:8888
login foo
password bar
"""
        cls.netrc_file = os.path.join(os.environ['HOME'], '.netrc')
        cls.password_file = resource_filename('TracRemote.tests',
                                              't/password.txt')
        cls.existing_netrc = os.path.exists(cls.netrc_file)
        if not cls.existing_netrc:
            with open(cls.netrc_file, 'w') as n:
                n.write(cls.netrc_data)
            os.chmod(cls.netrc_file, stat.S_IRUSR | stat.S_IWUSR)
        cls.trac = subprocess.Popen(['python', '-m',
                                     'TracRemote.tests.mock_trac_server'],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        time.sleep(5)

    @classmethod
    def tearDownClass(cls):
        cls.trac.kill()
        if not cls.existing_netrc:
            if os.path.exists(cls.netrc_file):
                os.remove(cls.netrc_file)

    def setUp(self):
        self.conn = Connection(self.url)

    def tearDown(self):
        pass

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
        """Test the index method.
        """
        ti = self.conn.index()
        self.assertEqual(ti[1], 'AAAS2016')
        self.assertEqual(ti[-1], 'testRST')
