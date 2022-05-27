===========
trac-remote
===========

Status
------

|Actions Status| |Coveralls Status| |Documentation Status|

.. |Actions Status| image:: https://github.com/weaverba137/trac-remote/workflows/CI/badge.svg
    :target: https://github.com/weaverba137/trac-remote/actions
    :alt: GitHub Actions CI Status

.. |Coveralls Status| image:: https://coveralls.io/repos/github/weaverba137/trac-remote/badge.svg?branch=main
    :target: https://coveralls.io/github/weaverba137/trac-remote?branch=main
    :alt: Test Coverage Status

.. |Documentation Status| image:: https://readthedocs.org/projects/trac-remote/badge/?version=latest
    :target: http://trac-remote.readthedocs.io/en/latest/
    :alt: Documentation Status

Description
-----------

trac-remote allows command-line manipulation of Trac_ instances,
similar to trac-admin_, but does not require physical, console
access to the Trac_ data.  In other words, trac-admin manipulates *local*
Trac servers, while trac-remote manipulates *remote* Trac servers.

History
-------

Portions of the back-end Python library were developed in the
SDSS-III_ `svn repository`_.  The present location of
the repository is http://github.com/weaverba137/trac-remote .


.. _Trac: http://trac.edgewall.org
.. _SDSS-III: http://www.sdss3.org
.. _`svn repository`: http://www.sdss3.org/dr10/software/products.php
.. _trac-admin: http://trac.edgewall.org/wiki/TracAdmin


License
-------

trac-remote is free software licensed under a 3-clause BSD-style license.
For details see the ``LICENSE.rst`` file.
