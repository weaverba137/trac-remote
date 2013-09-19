# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
def test_CRLF():
    from ..CRLF import CRLF
    text = "\n\n\nThis text\nContains\n\nUnix line-endings\n\n"
    crlf_text = CRLF(text)
    assert crlf_text == "This text\r\nContains\r\n\r\nUnix line-endings\r\n\r\n"
