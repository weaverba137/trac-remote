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
import sys


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
                        default=None,
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

    Returns
    -------
    :class:`str`
        Any output from the commands.
    """
    c = Connection(options.URL, options.password, options.realm,
                   options.debug)
    output = ''
    if options.cmd_name == 'attachment':
        if options.command == 'add':
            if len(options.arguments) < 3:
                c.attach(options.arguments[0], options.arguments[1],
                         replace=False)
            else:
                c.attach(options.arguments[0], options.arguments[1],
                         description=options.arguments[2], replace=False)
        if options.command == 'export':
            #
            # If a destination is specified, we *don't* want detach to save it.
            #
            if len(options.arguments) > 2:
                data = c.detach(options.arguments[0], options.arguments[1],
                                False)
                with open(options.arguments[2], 'wb') as f:
                    f.write(data)
            else:
                foo = c.detach(options.arguments[0], options.arguments[1],
                               True)
        if options.command == 'list':
            at = c.attachments(options.arguments[0])
            for fname in at:
                output += (fname + ("\t{size:d} bytes\t{author}\t{mtime}\t" +
                                    "{comment}").format(**at[fname]))
        if options.command == 'replace':
            if len(options.arguments) < 3:
                c.attach(options.arguments[0], options.arguments[1],
                         replace=True)
            else:
                c.attach(options.arguments[0], options.arguments[1],
                         description=options.arguments[2], replace=True)
    if options.cmd_name == 'wiki':
        if options.command == 'export':
            text = c.get(options.arguments[0])
            if len(options.arguments) > 1:
                with open(options.arguments[1], 'w') as t:
                    t.write(text)
            else:
                output = text
        if options.command == 'import' or options.command == 'replace':
            if len(options.arguments) > 1:
                if os.path.exists(options.arguments[1]):
                    with open(options.arguments[1], 'rb') as t:
                        text = t.read()
            else:
                text = sys.stdin.read()
            if len(options.arguments) > 2:
                c.set(options.arguments[0], text,
                      options.arguments[2])
            else:
                c.set(options.arguments[0], text)
        if options.command == 'list':
            title_index = c.index()
            output = "\n".join(title_index)+"\n"
    return output


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
    if options.password is not None:
        if not os.path.exists(options.password):
            print('Password file {0} is missing!'.format(options.password))
            return 2
    output = dispatch(options)
    if output:
        print(output)
    return 0
