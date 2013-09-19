# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
#
#
#
class SimpleIndexHTMLParser(HTMLParser):
    """Parse the Trac TitleIndex page

    Attributes
    ----------
    None
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.found_h1 = False
        self.h1_id = 'TitleIndex'
        self.found_list = False
        self.TitleIndex = list()
        return
    def handle_starttag(self, tag, attrs):
        if self.found_h1:
            if self.found_list:
                if tag == 'a':
                    self.TitleIndex.append(attrs[0][1].replace('/wiki/',''))
            else:
                if tag == 'ul':
                    self.found_list = True
        else:
            if tag == 'h1':
                #
                # Search for the id
                #
                dattrs = dict(attrs)
                try:
                    correct_id = (dattrs['id'] == self.h1_id)
                except KeyError:
                    correct_id = False
                self.found_h1 = correct_id
        return
    def handle_endtag(self, tag):
        if tag == 'ul' and self.found_h1:
            self.found_h1 = False
            self.found_list = False
        return
