# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
#
#
#
class SimpleWikiHTMLParser(HTMLParser):
    """Handle simple forms in Trac documents.  The form is searched
    for certain embedded values.

    Attributes
    ----------
    search_value : str
        The embedded value found in the form.  Initially set to ``None``.
    """
    def __init__(self,search='token'):
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
