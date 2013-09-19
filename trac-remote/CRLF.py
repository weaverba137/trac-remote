# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
def CRLF(text):
    """Convert Unix line endings to CRLF, which is required by the POST data
    mime-types application/x-www-form-urlencoded and multipart/form-data.

    Parameters
    ----------
    text : str
        Text to convert.

    Returns
    -------
    CRLF : str
        Input text converted to CRLF line endings.  Any initial blank lines
        are also removed.
    """
    crlf_text = text.replace( "\r\n", "\n" ).replace( "\r", "\n" ).replace( "\n", "\r\n" )
    while crlf_text[:2] == "\r\n":
        crlf_text = crlf_text[2:]
    return crlf_text
