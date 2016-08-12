# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""
=================================
TracRemote.tests.mock_trac_server
=================================

Simulate a Trac server.
"""
from pkg_resources import resource_filename
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler


class MockTracHandler(BaseHTTPRequestHandler):
    """Simulate a Trac server.
    """
    CRLF = '\r\n'
    login = resource_filename('TracRemote.tests', 't/login.html')
    index = resource_filename('TracRemote.tests', 't/TitleIndex.html')

    def do_GET(self):
        if self.path == '/login':
            with open(self.login, 'rb') as l:
                data = l.read()
            self.send_response(200)
            self.send_header('Set-Cookie',
                             ('trac_form_token=f5190f99a4efb5b1677f8230; ' +
                              'httponly; Path=/'))
            self.send_header('Set-Cookie',
                             ('trac_session=ThisIsATestSession; ' +
                              'httponly; Path=/'))
            self.send_header('Content-Type', 'text/html;charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        if self.path == '/wiki/TitleIndex':
            with open(self.index, 'rb') as l:
                data = l.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html;charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    def do_POST(self):
        if self.path == '/login':
            data = 'Cool.'+self.CRLF
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain;charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)


if __name__ == '__main__':
    httpd = HTTPServer(('', 8888), MockTracHandler)
    httpd.serve_forever()
