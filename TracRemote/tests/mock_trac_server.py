# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""
=================================
TracRemote.tests.mock_trac_server
=================================

Simulate a Trac server.
"""
from collections import OrderedDict
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
    edit = resource_filename('TracRemote.tests', 't/edit.html')
    attach = resource_filename('TracRemote.tests', 't/attach.html')
    passwd = resource_filename('TracRemote.tests', 't/password.txt')

    def do_GET(self):
        http_code = 200
        mime = 'text/html;charset=utf-8'
        extra_headers = list()
        if self.path == '/login':
            with open(self.login, 'rb') as l:
                data = l.read()
            extra_headers.append(('Set-Cookie', ('trac_form_token=' +
                                                 'f5190f99a4efb5b1677f8230; ' +
                                                 'httponly; Path=/')))
            extra_headers.append(('Set-Cookie', ('trac_session=' +
                                                 'ThisIsATestSession; ' +
                                                 'httponly; Path=/')))
        elif self.path == '/wiki/TitleIndex':
            with open(self.index, 'rb') as l:
                data = l.read()
        elif self.path.startswith('/wiki/TestEdit'):
            with open(self.edit, 'rb') as l:
                data = l.read()
        elif self.path.startswith('/attachment/wiki/TestAttach'):
            with open(self.attach, 'rb') as l:
                data = l.read()
        elif self.path.startswith('/raw-attachment/wiki/TestDetach'):
            with open(self.passwd, 'rb') as l:
                data = l.read()
            mime = 'application/octet-stream'
        elif self.path.startswith('/wiki/TestGet'):
            data = ('This is a test.'+self.CRLF).encode('utf-8')
            mime = 'text/plain;charset=utf-8'
        else:
            http_code = 404
            data = ('Not found!'+self.CRLF).encode('utf-8')
            mime = 'text/plain;charset=utf-8'
        self.send_response(http_code)
        if extra_headers:
            for h in extra_headers:
                self.send_header(*h)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        http_code = 200
        mime = 'text/plain;charset=utf-8'
        extra_headers = list()
        if self.path == '/login':
            data = ('This is a test.'+self.CRLF).encode('utf-8')
        elif self.path.startswith('/wiki/TestEdit'):
            data = ('This is a test.'+self.CRLF).encode('utf-8')
        else:
            http_code = 404
            data = ('Not found!'+self.CRLF).encode('utf-8')
        self.send_response(http_code)
        if extra_headers:
            for h in extra_headers:
                self.send_header(*h)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == '__main__':
    httpd = HTTPServer(('', 8888), MockTracHandler)
    httpd.serve_forever()
