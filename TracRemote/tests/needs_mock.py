# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""
===========================
TracRemote.tests.needs_mock
===========================

Contains a superclass for test cases that need a mock Trac server running.
"""
import unittest
import os
import stat
import subprocess
import time
from pkg_resources import resource_filename
from ..connection import Connection


class NeedsMock(unittest.TestCase):
    """Superclass for test cases that need a mock Trac server running.
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
