# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
from __future__ import print_function
#
def main():
    """Main entry point for the trac-remote script."""
    description = """Foo Bar"""
    try:
        import argparse
        parser = argparse.ArgumentParser(description=description)
    except ImportError:
        import optparse
        parser = optparse.OptionParser(usage=description)
    parser.parse_args()
    print("Foo Bar")
    return
