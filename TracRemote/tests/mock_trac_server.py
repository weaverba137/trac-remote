# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""
=================================
TracRemote.tests.mock_trac_server
=================================

Simulate a Trac server.
"""
from pkg_resources import resource_filename
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler


class MockTracHandler(BaseHTTPRequestHandler):
    """Simulate a Trac server.
    """
    CRLF = '\r\n'
    login = resource_filename('TracRemote.tests', 't/login.html')

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        if self.path == '/login':
            with open(self.login) as l:
                data = l.read()
            self.wfile.write(data)
        # self.wfile.write(self.path+self.CRLF)


if __name__ == '__main__':
    httpd = HTTPServer(('', 8888), MockTracHandler)
    httpd.serve_forever()
