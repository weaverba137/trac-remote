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


def main():
    """Main entry point for the trac-remote script.

    Returns
    -------
    :class:`int`
        An integer suitable for passing to :func:`sys.exit`.
    """
    import argparse
    description = """Foo Bar"""
    parser = argparse.ArgumentParser(description=description)
    parser.parse_args()
    print("Foo Bar")
    return 0
