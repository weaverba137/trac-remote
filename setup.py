#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function
#
# Standard imports
#
import os
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
setup_keywords['keywords'] = ['Trac']
setup_keywords['classifiers'] = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Framework :: Trac',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Topic :: Internet :: WWW/HTTP :: Site Management'
    ]
#
# Use README.rst as long_description.
#
setup_keywords['long_description'] = ''
if os.path.exists('README.rst'):
    with open('README.rst') as readme:
        setup_keywords['long_description'] = readme.read()
#
# Get version from __init__.py
#
try:
    from importlib import import_module
    product = import_module(setup_keywords['name'])
    setup_keywords['version'] = product.__version__
except ImportError:
    setup_keywords['version'] = '0.0.1.dev1'
#
# Set other keywords for the setup function.  These are automated, & should
# be left alone unless you are an expert.
#
# Treat everything in bin/ except *.rst as a script to be installed.
#
setup_keywords['provides'] = [setup_keywords['name']]
setup_keywords['python_requires'] = '>=2.7'
setup_keywords['zip_safe'] = True
setup_keywords['use_2to3'] = False
setup_keywords['packages'] = find_packages()
setup_keywords['cmdclass'] = {'sdist': DistutilsSdist}
setup_keywords['test_suite'] = 'TracRemote.tests.TracRemote_test_suite'
#
# Autogenerate command-line scripts.
#
setup_keywords['entry_points'] = {'console_scripts':
                                  ['trac-remote = TracRemote.main:main']}
#
# Add internal data directories.
#
setup_keywords['package_data'] = {'TracRemote.tests': ['t/*']}
#
# Run setup command.
#
setup(**setup_keywords)
