# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
#
#
#
class SimpleIndexHTMLParser(HTMLParser):
    """Parse the Trac TitleIndex page.

    This parser should be capable of handling Trac 1.0-style Index pages
    as well as older versions.

    Attributes
    ----------
    None
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.found_h1 = None
        self.h1_attr = {'h1':'id','div':'class'}
        self.h1_id = {'h1':'TitleIndex','div':'titleindex'}
        self.TitleIndex = list()
        return
    def handle_starttag(self, tag, attrs):
        if self.found_h1 is not None:
            if tag == 'a':
                self.TitleIndex.append(attrs[0][1].replace('/wiki/',''))
        else:
            if tag == 'h1' or tag =='div':
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
