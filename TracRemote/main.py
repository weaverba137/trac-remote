# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""
===============
TracRemote.main
===============

Contains entry point for command-line scripts.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from .connection import Connection


def main_args(args=None):
    """Parse the command-line arguments passed to :func:`main`.

    Parameters
    ----------
    args : :class:`list`, optional
        Set the command-line arguments for testing purposes.  Normally
        ``sys.argv`` will be parsed.

    Returns
    -------
    :class:`argparse.Namespace`
        An object containing the parsed arguments.
    """
    from argparse import ArgumentParser, RawTextHelpFormatter, SUPPRESS
    from . import __version__ as tr_version
    description = """trac-remote - The Trac Remote Administration Tool {0}.
""".format(tr_version)
    attachment_help = """add: attach a file to a wiki page.
export: grab an attachment from a wiki page and save it to a file.
list: list attachments on a wiki page.
replace: replace an existing attachment.
"""
    wiki_help = """export: save a wiki page to a text file.
import: create a new wiki page from a text file.
list: list wiki pages.
replace: replace an existing page with a text file.
"""
    parser = ArgumentParser(description=description,
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument('URL', help="URL for Trac instance.")
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s '+tr_version)
    subparsers = parser.add_subparsers(dest='cmd_name')
    parser_attach = subparsers.add_parser('attachment',
                                          formatter_class=RawTextHelpFormatter,
                                          help='Manage attached files.')
    parser_attach.add_argument('command',
                               choices=['add', 'export', 'list', 'replace'],
                               help=attachment_help)
    parser_wiki = subparsers.add_parser('wiki',
                                        formatter_class=RawTextHelpFormatter,
                                        help='Manage wiki pages.')
    parser_wiki.add_argument('command',
                             choices=['export', 'import', 'list', 'replace'],
                             help=wiki_help)
    if args is None:
        options = parser.parse_args()
    else:
        options = parser.parse_args(args)
    return options


def main():
    """Main entry point for the trac-remote script.

    Returns
    -------
    :class:`int`
        An integer suitable for passing to :func:`sys.exit`.
    """
    options = main_args()
    print(options)
    return 0
