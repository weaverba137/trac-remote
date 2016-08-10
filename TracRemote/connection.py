# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""
=====================
TracRemote.connection
=====================

Contains a class for establishing and using connections to Trac servers.
"""
from __future__ import absolute_import, division, print_function
try:
    from http.cookiejar import LWPCookieJar
except ImportError:
    from cookielib import LWPCookieJar
try:
    from urllib.parse import unquote, urlencode
except ImportError:
    from urllib import unquote, urlencode
try:
    from urllib.request import (build_opener, HTTPCookieProcessor,
                                HTTPDigestAuthHandler, Request)
except ImportError:
    from urllib2 import (build_opener, HTTPCookieProcessor,
                         HTTPDigestAuthHandler, Request)
from .util import (CRLF, SimpleAttachmentHTMLParser, SimpleIndexHTMLParser,
                   SimpleWikiHTMLParser)


class Connection(object):
    """A representation of the connection to Trac.

    Parameters
    ----------
    url : :class:`str`
        The base URL of the Trac server.
    passfile : :class:`str`, optional
        A file containing username and password.  Overrides ~/.netrc
    realm : :class:`str`, optional
        If the Trac instance uses basic or digest authentication, set this
        to the authentication realm
    debug : :class:`bool`, optional
        If set to ``True``, print more information.
    """

    def __init__(self, url=None, passfile=None, realm=None, debug=False):
        self._realm = realm
        self._debug = debug
        #
        # Cookies are necessary to maintain connection during script.
        #
        # Taken from:
        # http://www.voidspace.org.uk/python/articles/cookielib.shtml
        #
        cj = LWPCookieJar()
        self.opener = build_opener(HTTPCookieProcessor(cj))
        # install_opener(opener)
        #
        # Handle login
        #
        if url is None:
            raise ValueError("A Trac URL is required!")
        self.url = url
        foo = self.url.split('/')
        self._baseurl = foo[0] + '//' + foo[2]
        if passfile is None:
            user, password = self._readPasswordNetrc(self._baseurl)
        else:
            user, password = self._readPassword(passfile)
        if password is None:
            raise ValueError(('Could not find a password for ' +
                              '{0}!').format(self.url))
        parser = SimpleWikiHTMLParser()
        if self._realm is not None:
            auth_handler = HTTPDigestAuthHandler()
            auth_handler.add_password(realm=self._realm,
                                      uri=self.url,
                                      user=user,
                                      passwd=password)
            self.opener.add_handler(auth_handler)
        response = self.opener.open(self.url + "/login")
        if self._debug:
            print(response.info())
        parser.feed(response.read())
        response.close()
        self._form_token = parser.search_value
        if self._realm is None:
            postdata = {'user': user,
                        'password': password,
                        '__FORM_TOKEN': self._form_token,
                        'referer': ''}
            #
            # The cookie named 'trac_auth' is obtained after the POST to the
            # login page but before the redirect to the wiki front page.
            # Technically it is obtained in the HTTP headers of the redirect.
            #
            response = self.opener.open(self.url+"/login", urlencode(postdata))
            if self._debug:
                print(response.info())
            response.close()
        self._cookies = list()
        for cookie in cj:
            if self._debug:
                print(cookie)
            self._cookies.append((cookie.name, cookie.value))
            if cookie.name == 'trac_form_token' and self._form_token is None:
                self._form_token = cookie.value
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
            user = (pf.readline()).strip()
            password = (pf.readline()).strip()
        return (user, password)

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
            user, account, password = rc.hosts[trachost]
        except KeyError:
            return None
        return (user, password)

    def index(self):
        """Get and parse the TitleIndex page.

        Returns
        -------
        index : :class:`list`
            A list of all Trac wiki pages.
        """
        response = self.opener.open(self.url + "/wiki/TitleIndex")
        titleindex = response.read()
        response.close()
        parser = SimpleIndexHTMLParser()
        parser.feed(titleindex)
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
        response = self.opener.open(self.url+"/wiki/"+pagepath+"?format=txt")
        txt = response.read()
        response.close()
        # try:
        #     utxt = unicode(txt,'utf-8')
        # except UnicodeDecodeError:
        #     return txt
        return txt

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
        response = self.opener.open(self.url+"/wiki/"+pagepath+"?action=edit")
        if self._debug:
            print(response.info())
        parser = SimpleWikiHTMLParser('version')
        parser.feed(response.read())
        response.close()
        postdata = {'__FORM_TOKEN': self._form_token,
                    'from_editor': '1',
                    'action': 'edit',
                    'version': parser.search_value,
                    'save': 'Submit changes',
                    'text': CRLF(text)}
        if comment is not None:
            postdata['comment'] = CRLF(comment)
        if self._debug:
            print(urlencode(postdata))
        response = self.opener.open(self.url+"/wiki/"+pagepath,
                                    urlencode(postdata))
        response.close()
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
        response = self.opener.open(self.url+"/attachment/wiki/"+pagepath+"/")
        attachmentindex = response.read()
        response.close()
        parser = SimpleAttachmentHTMLParser()
        parser.feed(attachmentindex)
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
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from httplib import HTTPConnection, HTTPSConnection
        from os.path import basename
        if self._realm is not None:
            response = self.opener.open(self.url + "/attachment/wiki/" +
                                        pagepath + "/?action=new")
            if self._debug:
                print(response.info())
                print(response.read())
            response.close()
        #
        # Read and examine the file
        #
        if isinstance(filename, tuple):
            fname = basename(filename[0])
            fbytes = filename[1]
        else:
            with open(filename, 'r') as f:
                fbytes = f.read()
            fname = basename(filename)
        #
        # Create the mime sections to hold the form data
        #
        postdata = MIMEMultipart('form-data')
        postdict = {'__FORM_TOKEN': self._form_token,
                    'action': 'new',
                    'realm': 'wiki',
                    'id': pagepath,
                    }
        if description is not None:
            postdict['description'] = description
        if replace:
            postdict['replace'] = 'on'
        for k in postdict:
            mime = MIMEText(postdict[k])
            mime['Content-disposition'] = 'form-data; name="{0}"'.format(k)
            del mime['MIME-Version']
            del mime['Content-Type']
            del mime['Content-Transfer-Encoding']
            postdata.attach(mime)
        del postdata['MIME-Version']
        body = postdata.as_string().split('\n')
        if self._debug:
            print(body)
        #
        # Create a separate mime section for the file by hand.
        #
        payload = ['--'+postdata.get_boundary()]
        payload.append(('Content-disposition: form-data; ' +
                        'name="attachment"; ' +
                        'filename="{0}"').format(unquote(fname)))
        payload.append('Content-type: application/octet-stream')
        payload.append('')
        payload.append(fbytes)
        payload.append('--'+postdata.get_boundary()+'--')
        content_header = (body[0]+body[1]).split(': ')[1]
        if self._debug:
            print(content_header)
        crlf_body = '\r\n'.join(body[2:len(body)-1] + payload)+'\r\n'
        if self._debug:
            print(crlf_body)
        #
        # Have to use a raw httplib connection becuase urlopen will
        # try to encode the data as application/x-www-form-urlencoded
        #
        if 'https' in self.url:
            if self._debug:
                HTTPSConnection.debuglevel = 1
            hostname = self.url[self.url.index('//')+2:]
            if hostname.find('/') > 0:
                foo = hostname.split('/')
                hostname = foo[0]
                extra = '/'+'/'.join(foo[1:])
            else:
                extra = ''
            http = HTTPSConnection(hostname)
        else:
            if self._debug:
                HTTPConnection.debuglevel = 1
            hostname = self.url[self.url.index('//')+2:]
            if hostname.find('/') > 0:
                foo = hostname.split('/')
                hostname = foo[0]
                extra = '/'+'/'.join(foo[1:])
            else:
                extra = ''
            http = HTTPConnection(hostname)
        headers = {'Cookie': '; '.join(['='.join(c) for c in self._cookies]),
                   'Content-Type': content_header}
        if self._realm is not None:
            auth_handler = 0
            while not isinstance(self.opener.handlers[auth_handler],
                                 HTTPDigestAuthHandler):
                auth_handler += 1
            req = Request((self.url + "/attachment/wiki/" + pagepath +
                           "/?action=new"), 'foo=bar')
            req_data = {'realm': self._realm,
                        'nonce': self.opener.handlers[auth_handler].last_nonce,
                        'qop': 'auth'}
            auth_string = self.opener.handlers[auth_handler].get_authorization(
                req, req_data)
            if self._debug:
                print(auth_string)
            # http.putheader('Authorization', 'Digest '+auth_string)
            headers['Authorization'] = 'Digest ' + auth_string
        http.request('POST', extra+"/attachment/wiki/"+pagepath+"/?action=new",
                     crlf_body, headers)
        #
        # If successful, the initial response should be a redirect.
        #
        response = http.getresponse()
        if self._debug:
            print(response.getheaders())
            print(response.status)
            print(response.read())
        http.close()
        return

    def detach(self, pagepath, filename, save=True):
        """Grab a file attached to a wiki page.

        Parameters
        ----------
        pagepath : :class:`str`
            Wiki page to attach to.
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
        from os.path import basename
        #
        # Construct url for attachment
        #
        fullurl = (self.url + '/raw-attachment/wiki/' + pagepath + '/' +
                   basename(filename))
        #
        # Get the file
        #
        response = self.opener.open(fullurl)
        data = response.read()
        response.close()
        #
        # Write the file
        #
        if save:
            ff = unquote(filename)
            with open(ff, 'w') as f:
                f.write(data)
        return data
