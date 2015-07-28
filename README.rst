Python collection filter
========================

https://github.com/kudo/collection-filter

|Build Status| |Unit Test Coverage|

This library provides a DSL filter for list or dict data.
It is original designed for RESTful API partial response.
Tested with Python 2.6, 2.7. 

Quick Start
-----------

To install, use pip:

::

    $ pip install collection-filter

Then:

.. code:: python

    $ python

    >>> from collection_filter import collection_filter

    # Query a dict
    >>> collection_filter({'foo': 1, 'bar': 2}, 'foo')
    {'foo': 1}

    # Query a dict with multiple elements (seperated by comma)
    >>> collection_filter({'foo': 1, 'bar': 2}, 'foo,bar')
    {'foo': 1, 'bar': 2}

    # Query a dict deeply
    >>> collection_filter({'foo': {'bar': 2, 'orange': 'sweet'}}, 'foo.bar')
    {'foo': {'bar': 2}}

    # Query a list
    >>> collection_filter([{'foo': 1, 'bar': 2}, {'foo': 3, 'bar': 4}], '[].foo')
    [{'foo': 1}, {'foo': 3}]

    # list/dict combination example
    >>> collection_filter({'foo': 'bar', 'aListOfDict': [{'foo': 1, 'bar': 2}], 'aListOfDict[].foo')
    {'aListOfDict': [{'foo': 1}]}


Syntax
---------------

Currently support operators

+----------+------------------------------------------------+
| Operator | Description                                    |  
+==========+================================================+
| ,        | Multiple field query sperated by comma         |
+----------+------------------------------------------------+
| []       | To indicate the data should be handled as list |
+----------+------------------------------------------------+
| .        | Dot notation should follow with a symbol name  |
|          | which to specify a field in current dict data  |
+----------+------------------------------------------------+

 
Copyright and License
---------------------

Copyright 2015, Kudo Chien

Licensed under a `MIT license`_.

.. |Build Status| image:: https://travis-ci.org/Kudo/collection-filter.svg?branch=master
   :target: https://travis-ci.org/Kudo/collection-filter

.. |Unit Test Coverage| image:: https://coveralls.io/repos/Kudo/collection-filter/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/Kudo/collection-filter?branch=master

.. _MIT license: http://opensource.org/licenses/MIT
