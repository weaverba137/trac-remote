# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""
===============
TracRemote.util
===============

Utility functions and classes for internal use by the TracRemote package.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from HTMLParser import HTMLParser


def CRLF(text):
    """Convert Unix line endings to CRLF, which is required by the POST data
    mime-types application/x-www-form-urlencoded and multipart/form-data.

    Parameters
    ----------
    text : :class:`str`
        Text to convert.

    Returns
    -------
    :class:`str`
        Input text converted to CRLF line endings.  Any initial blank lines
        are also removed.
    """
    crlf_text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\n",
                                                                       "\r\n")
    while crlf_text[:2] == "\r\n":
        crlf_text = crlf_text[2:]
    return crlf_text


class SimpleAttachmentHTMLParser(HTMLParser):
    """Parse an attachment list page
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.found_div = False
        self.div_id = 'attachments'
        self.found_list = False
        self.found_comment = False
        self.attachments = dict()
        self.current_attachment = None
        return

    def handle_starttag(self, tag, attrs):
        if self.found_div:
            if self.found_list:
                dattrs = dict(attrs)
                if tag == 'a':
                    try:
                        if dattrs['title'] == 'View attachment':
                            ca = dattrs['href'].split('/')[-1]
                            a = {'size': 0, 'mtime': ''}
                            self.current_attachment = ca
                            self.attachments[self.current_attachment] = a
                        else:
                            mtime = dattrs['title'].split(' ')[0]
                            foo = self.attachments[self.current_attachment]
                            foo['mtime'] = mtime
                    except KeyError:
                        pass
                if tag == 'span':
                    try:
                        size = int(dattrs['title'].split(' ')[0])
                    except:
                        size = 0
                    self.attachments[self.current_attachment]['size'] = size
                if tag == 'dd':
                    self.found_comment = True
            else:
                if tag == 'dl':
                    self.found_list = True
        else:
            if tag == 'div':
                #
                # Search for the id
                #
                dattrs = dict(attrs)
                try:
                    correct_id = (dattrs['id'] == self.div_id)
                except KeyError:
                    correct_id = False
                self.found_div = correct_id
        return

    def handle_data(self, data):
        if self.found_comment:
            self.attachments[self.current_attachment]['comment'] = data.strip()
        return

    def handle_endtag(self, tag):
        if tag == 'dl' and self.found_div:
            self.found_div = False
            self.found_list = False
        if tag == 'dd' and self.found_comment:
            self.found_comment = False
        return


class SimpleIndexHTMLParser(HTMLParser):
    """Parse the Trac TitleIndex page.

    This parser should be capable of handling Trac 1.0-style Index pages
    as well as older versions.
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.found_h1 = None
        self.h1_attr = {'h1': 'id', 'div': 'class'}
        self.h1_id = {'h1': 'TitleIndex', 'div': 'titleindex'}
        self.TitleIndex = list()
        return

    def handle_starttag(self, tag, attrs):
        if self.found_h1 is not None:
            if tag == 'a':
                self.TitleIndex.append(attrs[0][1].replace('/wiki/', ''))
        else:
            if tag == 'h1' or tag == 'div':
                #
                # Search for the id
                #
                dattrs = dict(attrs)
                correct_id = None
                try:
                    if (dattrs[self.h1_attr[tag]] == self.h1_id[tag]):
                        correct_id = tag
                except KeyError:
                    pass
                self.found_h1 = correct_id
        return

    def handle_endtag(self, tag):
        if tag == 'ul' and self.found_h1 == 'h1':
            self.found_h1 = None
        if tag == 'div' and self.found_h1 == 'div':
            self.found_h1 = None
        return


class SimpleWikiHTMLParser(HTMLParser):
    """Handle simple forms in Trac documents.  The form is searched
    for certain embedded values.

    Attributes
    ----------
    search_value : :class:`str`
        The embedded value found in the form.  Initially set to ``None``.
    """

    def __init__(self, search='token'):
        HTMLParser.__init__(self)
        self.found_form = False
        self.search_value = None
        self.search = search
        if search == 'token':
            self.form_id = 'acctmgr_loginform'
            self.input_name = '__FORM_TOKEN'
        else:
            self.form_id = 'edit'
            self.input_name = 'version'
        return

    def handle_starttag(self, tag, attrs):
        if self.found_form:
            if tag == 'input':
                dattrs = dict(attrs)
                try:
                    found_token = (dattrs['name'] == self.input_name)
                except KeyError:
                    found_token = False
                if found_token:
                    self.search_value = dattrs['value']
        else:
            if tag == 'form':
                #
                # Search for the id
                #
                dattrs = dict(attrs)
                try:
                    correct_id = (dattrs['id'] == self.form_id)
                except KeyError:
                    correct_id = False
                self.found_form = correct_id
        return

    def handle_endtag(self, tag):
        if tag == 'form' and self.found_form:
            self.found_form = False
        return
