# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""
=====================
TracRemote.connection
=====================

Contains a class for establishing and using connections to Trac servers.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from os.path import basename
import requests as r
# try:
#     from http.cookiejar import LWPCookieJar
# except ImportError:
#     from cookielib import LWPCookieJar
# try:
#     from urllib.parse import unquote, urlencode
# except ImportError:
#     from urllib import unquote, urlencode
# try:
#     from urllib.request import (build_opener, HTTPCookieProcessor,
#                                 HTTPDigestAuthHandler, Request)
# except ImportError:
#     from urllib2 import (build_opener, HTTPCookieProcessor,
#                          HTTPDigestAuthHandler, Request)
from .util import (CRLF, SimpleAttachmentHTMLParser, SimpleIndexHTMLParser,
                   SimpleWikiHTMLParser)


class Connection(object):
    """A representation of the connection to Trac.

    Parameters
    ----------
    url : :class:`str`
        The base URL of the Trac server.
    passfile : :class:`str`, optional
        A file containing username and password.  Overrides ~/.netrc.
    realm : :class:`str`, optional
        If the Trac instance uses basic or digest authentication, set this
        to the authentication realm.
    debug : :class:`bool`, optional
        If set to ``True``, print more information.
    """

    def __init__(self, url=None, passfile=None, realm=None, debug=False):
        self._realm = realm
        self._debug = debug
        #
        # Handle login
        #
        if url is None:
            raise ValueError("A Trac URL is required!")
        self.url = url
        foo = self.url.split('/')
        self._baseurl = foo[0] + '//' + foo[2]
        if passfile is None:
            username, password = self._readPasswordNetrc(self._baseurl)
        else:
            username, password = self._readPassword(passfile)
        if password is None:
            raise ValueError(('Could not find a password for ' +
                              '{0}!').format(self.url))
        # parser = SimpleWikiHTMLParser()
        # if self._realm is not None:
        #     auth_handler = HTTPDigestAuthHandler()
        #     auth_handler.add_password(realm=self._realm,
        #                               uri=self.url,
        #                               user=username,
        #                               passwd=password)
        #     self.opener.add_handler(auth_handler)
        response = r.get(self.url + "/login")
        self._cookies = response.cookies
        if self._debug:
            print(response.request.headers)
            print(response.status_code)
            print(response.headers)
        assert 'trac_form_token' in self._cookies
        self._form_token = self._cookies['trac_form_token']
        if self._realm is None:
            postdata = {'username': username,
                        'password': password,
                        '__FORM_TOKEN': self._form_token,
                        'referer': self.url + "/login"}
            response = r.post(self.url + "/login", data=postdata,
                              cookies=self._cookies)
            if self._debug:
                print(response.request.headers)
                print(response.status_code)
                print(response.headers)
            #
            # The cookie named 'trac_auth' is obtained after the POST to the
            # login page but before the redirect to the wiki front page.
            # Technically it is obtained in the HTTP headers of the redirect.
            #
            self._cookies.update(response.history[0].cookies)
        assert 'trac_auth' in self._cookies
        # self._cookies = list()
        # for cookie in cj:
        #     if self._debug:
        #         print(cookie)
        #     self._cookies.append((cookie.name, cookie.value))
        #     if cookie.name == 'trac_form_token' and self._form_token is None:
        #         self._form_token = cookie.value
        return

    def _readPassword(self, passfile):
        """Read the password file & return the username & password.

        Parameters
        ----------
        passfile : :class:`str`
            File containing Trac username and password.

        Returns
        -------
        :func:`tuple`
            A tuple containing the username and password.
        """
        with open(passfile, 'r') as pf:
            username = (pf.readline()).strip()
            password = (pf.readline()).strip()
        return (username, password)

    def _readPasswordNetrc(self, url):
        """Read the Trac username and password from a .netrc file.

        Parameters
        ----------
        url : :class:`str`
            URL of the Trac server

        Returns
        -------
        :func:`tuple`
            A tuple containing the username and password.  If there is no
            .netrc file, or if the Trac server is not present,
            returns ``None``.
        """
        from netrc import netrc
        try:
            rc = netrc()
        except IOError:
            return None
        trachost = url[url.index('//')+2:]
        if trachost.find('/') > 0:
            foo = hostname.split('/')
            trachost = foo[0]
        try:
            username, account, password = rc.hosts[trachost]
        except KeyError:
            return None
        return (username, password)

    def index(self):
        """Get and parse the TitleIndex page.

        Returns
        -------
        index : :class:`list`
            A list of all Trac wiki pages.
        """
        response = r.get(self.url + "/wiki/TitleIndex", cookies=self._cookies)
        if self._debug:
            print(response.request.headers)
            print(response.status_code)
            print(response.headers)
        parser = SimpleIndexHTMLParser()
        parser.feed(response.text)
        return parser.TitleIndex

    def get(self, pagepath):
        """Requests a wiki page in text format.

        Parameters
        ----------
        pagepath : :class:`str`
            Wiki page to grab.

        Returns
        -------
        :class:`str`
            The text of the wiki page.  Note that in some cases, the text of
            the page may contain UTF-8 characters, so a further conversion to
            unicode may be warranted. The text may also contain Windows
            (CRLF) line endings.
        """
        response = r.get(self.url + "/wiki/" + pagepath + "?format=txt",
                         cookies=self._cookies)
        if self._debug:
            print(response.request.headers)
            print(response.status_code)
            print(response.headers)
        return response.text

    def set(self, pagepath, text, comment=None):
        """Inputs text into the wiki input text box.

        Parameters
        ----------
        pagepath : :class:`str`
            Wiki page to update.
        text : :class:`str`
            The wiki text.
        comment : :class:`str`, optional
            A comment on the change.
        """
        response = r.get(self.url + "/wiki/" + pagepath + "?action=edit",
                         cookies=self._cookies)
        if self._debug:
            print(response.request.headers)
            print(response.status_code)
            print(response.headers)
        parser = SimpleWikiHTMLParser('version')
        parser.feed(response.text)
        postdata = {'__FORM_TOKEN': self._form_token,
                    'from_editor': '1',
                    'action': 'edit',
                    'version': parser.search_value,
                    'save': 'Submit changes',
                    'text': CRLF(text)}
        if comment is not None:
            postdata['comment'] = CRLF(comment)
        response = r.post(self.url + "/wiki/" + pagepath,
                          data=postdata,
                          cookies=self._cookies)
        if self._debug:
            print(response.request.headers)
            print(response.status_code)
            print(response.headers)
        return

    def attachments(self, pagepath):
        """Return a list of files attached to a particular page.

        Parameters
        ----------
        pagepath : :class:`str`
            Wiki page to attach to.

        Returns
        -------
        :class:`dict`
            A dictionary where the keys are file names and the values are
            sub-dictionaries that contain the size and mtime of the file.
            If there are no attachments, the dictionary will be empty.
        """
        response = r.get(self.url + "/attachment/wiki/" + pagepath + "/",
                         cookies=self._cookies)
        if self._debug:
            print(response.request.headers)
            print(response.status_code)
            print(response.headers)
        parser = SimpleAttachmentHTMLParser()
        parser.feed(response.text)
        return parser.attachments

    def attach(self, pagepath, filename, description=None, replace=False):
        """Attaches a file to a wiki page.

        Parameters
        ----------
        pagepath : :class:`str`
            Wiki page to attach to.
        filename : :class:`str` or :func:`tuple`
            Name of the file to attach.  If a tuple is passed, the first item
            should be the name of the file, & the second item should be the
            data that the file should contain.
        description : :class:`str`, optional
            If supplied, this description will be added as a comment on the
            attachment.
        replace : :class:`bool`, optional
            Set this to ``True`` if the file is replacing an existing file.
        """
        # from email.mime.multipart import MIMEMultipart
        # from email.mime.text import MIMEText
        # from httplib import HTTPConnection, HTTPSConnection
        # if self._realm is not None:
        #     response = self.opener.open(self.url + "/attachment/wiki/" +
        #                                 pagepath + "/?action=new")
        #     if self._debug:
        #         print(response.info())
        #         print(response.read())
        #     response.close()
        #
        # Read and examine the file
        #
        if isinstance(filename, tuple):
            fname = basename(filename[0])
            fbytes = filename[1]
        else:
            with open(filename, 'rb') as f:
                fbytes = f.read()
            fname = basename(filename)
        files = {'attachment': (fname, fbytes),
                 '__FORM_TOKEN': self._form_token,
                 'action': 'new',
                 'realm': 'wiki',
                 'id': pagepath}
        if description is not None:
            files['description'] = description
        if replace:
            files['replace'] = 'on'
        p = r.Request('POST', self.url + "/attachment/wiki/" +
                      pagepath + "/?action=new", files=files,
                      cookies=self._cookies)
        prepared = p.prepare()
        print(prepared.headers)
        print(prepared.body)
        # response = r.post(self.url + "/attachment/wiki/" +
        #                   pagepath + "/?action=new", files=files,
        #                   cookies=self._cookies)
        #
        # If successful, the initial response should be a redirect.
        #
        # if self._debug:
        #     print(response.request.headers)
        #     print(response.status_code)
        #     print(response.headers)
        return

    def detach(self, pagepath, filename, save=True):
        """Grab a file attached to a wiki page.

        Parameters
        ----------
        pagepath : :class:`str`
            Wiki page that contains attached file.
        filename : :class:`str`
            Name of the file to read. The name had better match an
            actual attached file!
        save : :class:`bool`, optional
            If set to ``False``, no file will be saved, but the data will still
            be returned.

        Returns
        -------
        :class:`str`
            The raw data read from the file.
        """
        #
        # Construct url for attachment
        #
        fullurl = (self.url + '/raw-attachment/wiki/' + pagepath + '/' +
                   basename(filename))
        #
        # Get the file
        #
        response = r.get(fullurl, cookies=self._cookies)
        if self._debug:
            print(response.request.headers)
            print(response.status_code)
            print(response.headers)
        #
        # Write the file
        #
        if save:
            ff = unquote(filename)
            with open(ff, 'wb') as f:
                f.write(response.content)
        return response.content

    def close(self):
        """Close the connection by logging out.
        """
        response = r.get(self.url + '/logout', cookies=self._cookies)
        if self._debug:
            print(response.request.headers)
            print(response.status_code)
            print(response.headers)
        return

    logout = close
