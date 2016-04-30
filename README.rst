=======
pychurn
=======

Installation
------------

::

    pip install -U pychurn

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
