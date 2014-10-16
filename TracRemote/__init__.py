# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""
==========
TracRemote
==========

This package provides a mechanism to manipulate remote
Trac_ instances similar to trac-admin_.

.. _Trac: http://trac.edgewall.org
.. _trac-admin: http://trac.edgewall.org/wiki/TracAdmin
"""
#
#
#
from __future__ import absolute_import, unicode_literals
#
#
#
from .connection import connection
from .CRLF import CRLF
from .main import main
from .SimpleAttachmentHTMLParser import SimpleAttachmentHTMLParser
from .SimpleIndexHTMLParser import SimpleIndexHTMLParser
from .SimpleWikiHTMLParser import SimpleWikiHTMLParser
#
#
#
__all__ = [ 'connection' ]
__version__ = '0.0.1'
