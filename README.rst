=======
pychurn
=======

.. image:: https://img.shields.io/travis/jmcarp/pychurn/master.svg
    :target: https://travis-ci.org/jmcarp/pychurn
    :alt: Travis-CI

Installation
------------

::

    pip install -U pychurn

pychurn will use the `pygit2` bindings for `libgit2` if available, which significantly improves performance. To install, see the `libgit2 docs <http://www.pygit2.org/install.html>`_.

Usage
-----

Read the docs: ::

    pychurn --help

Example usage: ::

    pychurn report
    pychurn report --path /path/to/repo --since 2016-01-01 --exclude '**test**'

Example output: ::

    $ pychurn --debug report --path . --sort churn --count 5

    code                                    churn    complexity
    ------------------------------------  -------  ------------
    pychurn/version.py:get_churn                4            11
    pychurn/cli.py:churn                        3             2
    pychurn/complexity.py:get_complexity        3             8
    pychurn/cli.py:cli                          2             2
    pychurn/cli.py:report                       1             4
