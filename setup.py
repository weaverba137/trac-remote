#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function
#
# Standard imports
#
import glob
import os
import sys
import re
#
# setuptools' sdist command ignores MANIFEST.in
#
from distutils.command.sdist import sdist as DistutilsSdist
from setuptools import setup, find_packages
#
# Begin setup
#
setup_keywords = dict()
setup_keywords['name'] = 'TracRemote'
setup_keywords['description'] = ('Allows remote manipulation of Trac ' +
                                 'servers, similar to trac-admin.')
setup_keywords['author'] = 'Benjamin Alan Weaver'
setup_keywords['author_email'] = 'baweaver@lbl.gov'
setup_keywords['license'] = 'BSD'
setup_keywords['url'] = 'https://github.com/weaverba137/trac-remote'
setup_keywords['version'] = '0.0.2.dev1'
#
# Use README.rst as long_description.
#
setup_keywords['long_description'] = ''
if os.path.exists('README.rst'):
    with open('README.rst') as readme:
        setup_keywords['long_description'] = readme.read()
#
# Set other keywords for the setup function.  These are automated, & should
# be left alone unless you are an expert.
#
# Treat everything in bin/ except *.rst as a script to be installed.
#
setup_keywords['provides'] = [setup_keywords['name']]
setup_keywords['requires'] = ['Python (>2.7.0)']
# setup_keywords['install_requires'] = ['Python (>2.7.0)']
setup_keywords['zip_safe'] = False
setup_keywords['use_2to3'] = True
setup_keywords['packages'] = find_packages()
# setup_keywords['package_dir'] = {'':'py'}
setup_keywords['cmdclass'] = {'sdist': DistutilsSdist}
setup_keywords['test_suite'] = ('{name}.tests.{name}_test_suite.' +
                                '{name}_test_suite').format(**setup_keywords)
#
# Autogenerate command-line scripts.
#
setup_keywords['entry_points'] = {'console_scripts':
                                  ['trac-remote = TracRemote.main:main']}
#
# Add internal data directories.
#
# setup_keywords['package_data'] = {'specter': ['data/*'],
#                                   'specter.test': ['t/*']}
#
# Run setup command.
#
setup(**setup_keywords)
