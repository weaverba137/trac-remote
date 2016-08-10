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
import os


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
    attachment_help = """add <page> <path> [description]
    Attach a file to a wiki page. The author will be set using the login.

export <page> <name> [destination]
    Grab an attachment from a wiki page and save it to a file.

list <page>
    List attachments on a wiki page.

replace <page> <path> [description]
    Replace an existing attachment. The author will be set using the login.

"""
    wiki_help = """export <path> [filename]
    Save a wiki page to a text file or stdout.

import <path> [filename] [comment]
    Create a new wiki page from a text file or stdin.

list
    List wiki pages.

replace <path> [filename] [comment]
    Replace an existing page with a text file.

"""
    parser = ArgumentParser(description=description,
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument('URL', help="URL for Trac instance.")
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Enable debug output.')
    parser.add_argument('-p', '--password', metavar='FILE',
                        default=os.path.join(os.environ['HOME'], '.netrc'),
                        help=('Read password information from FILE ' +
                              'instead of %(default)s.'))
    parser.add_argument('-r', '--realm', metavar='REALM', default=None,
                        help=('Set basic or digest authentication realm, if ' +
                              'the Trac instance does not use its own ' +
                              'authentication mechanism.'))
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s '+tr_version)
    subparsers = parser.add_subparsers(dest='cmd_name')
    parser_attach = subparsers.add_parser('attachment',
                                          formatter_class=RawTextHelpFormatter,
                                          help='Manage attached files.')
    parser_attach.add_argument('command',
                               choices=['add', 'export', 'list', 'replace'],
                               help=attachment_help)
    parser_attach.add_argument('arguments', nargs='*',
                               help='Arguments to one of the commands above.')
    parser_wiki = subparsers.add_parser('wiki',
                                        formatter_class=RawTextHelpFormatter,
                                        help='Manage wiki pages.')
    parser_wiki.add_argument('command',
                             choices=['export', 'import', 'list', 'replace'],
                             help=wiki_help)
    parser_wiki.add_argument('arguments', nargs='*',
                             help='Arguments to one of the commands above.')
    if args is None:
        options = parser.parse_args()
    else:
        options = parser.parse_args(args)
    return options


def validate_args(options):
    """Validate the arguments to the various sub-commands.

    Parameters
    ----------
    options : :class:`argparse.Namespace`
        Parsed options.

    Returns
    -------
    :class:`bool`
        ``True`` if the arguments are valid.
    """
    nargs = {'attachment': {'add': 2, 'export': 2, 'list': 1, 'replace': 2},
             'wiki': {'export': 1, 'import': 1, 'list': 0, 'replace': 1}
             }
    return len(options.arguments) >= nargs[options.cmd_name][options.command]


def dispatch(options):
    """Determine function to run, given arguments.

    Parameters
    ----------
    options : :class:`argparse.Namespace`
        Parsed options.
    """
    print(("c = Connection('{0.URL}', '{0.password}', " +
           "{0.realm}, {0.debug})").format(options))
    if options.cmd_name == 'attachment':
        if options.command == 'add':
            print(("c.attach('{0}', '{1}', '{2}', " +
                   "False)").format(*options.arguments))
        if options.command == 'export':
            print("c.detach('{0}', '{1}', True)".format(*options.arguments))
        if options.command == 'list':
            print("c.attachments({0})".format(options.arguments[0]))
        if options.command == 'replace':
            print("c.attach('{0}', '{1}', '{2}', " +
                  "True)".format(*options.arguments))
    if options.cmd_name == 'wiki':
        if options.command == 'export':
            print("c.get('{0}')".format(*options.arguments))
        if options.command == 'import':
            print("c.set('{0}', '{1}', '{2}')".format(*options.arguments))
        if options.command == 'list':
            print("c.index()")
        if options.command == 'replace':
            print("c.set('{0}', '{1}', '{2}')".format(*options.arguments))
    # c = Connection(options.URL, options.password, options.realm,
    #                options.debug)
    return


def main():
    """Main entry point for the trac-remote script.

    Returns
    -------
    :class:`int`
        An integer suitable for passing to :func:`sys.exit`.
    """
    options = main_args()
    valid = validate_args(options)
    if not valid:
        print(('trac-remote: error: too few or invalid arguments to ' +
               '"{0.cmd_name} {0.command}"').format(options))
        return 1
    if not os.path.exists(options.password):
        print('Password file {0} is missing!'.format(options.password))
        return 2
    print(options)
    dispatch(options)
    return 0
