# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
#
#
#
class SimpleAttachmentHTMLParser(HTMLParser):
    """Parse an attachment list page

    Attributes
    ----------
    None
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
                            self.current_attachment = dattrs['href'].split('/')[-1]
                            self.attachments[self.current_attachment] = {'size':0,'mtime':''}
                        else:
                            mtime = dattrs['title'].split(' ')[0]
                            self.attachments[self.current_attachment]['mtime'] = mtime
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
