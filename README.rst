===========
Heritage.py
===========

.. image:: https://img.shields.io/pypi/v/heritage
        :target: https://pypi.python.org/pypi/heritage

.. image:: https://readthedocs.org/projects/heritage-py/badge/?version=latest
        :target: https://heritage-py.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/pypi/pyversions/heritage
        :target: https://pypi.python.org/pypi/heritage
        :alt: Python Version Support

.. image:: https://img.shields.io/github/issues/hrishikeshrt/heritage
        :target: https://github.com/hrishikeshrt/heritage/issues
        :alt: GitHub Issues

.. image:: https://img.shields.io/github/followers/hrishikeshrt?style=social
        :target: https://github.com/hrishikeshrt
        :alt: GitHub Followers

.. image:: https://img.shields.io/twitter/follow/hrishikeshrt?style=social
        :target: https://twitter.com/hrishikeshrt
        :alt: Twitter Followers


Heritage.py is a python interface to `The Sanskrit Heritage Site`_.

.. _`The Sanskrit Heritage Site`: https://sanskrit.inria.fr/index.en.html

* Free software: GNU General Public License v3
* Documentation: https://heritage-py.readthedocs.io.


Features
========

* Morphological Analysis
* Sandhi Formation
* Declensions
* Conjugations

Install
=======

To install Heritage.py, run this command in your terminal:

.. code-block:: console

    $ pip install heritage

Usage
=====

Heritage.py has two possible modes of operation,

1. Using a web mirror

This mode uses any compatible web mirror of The Heritage Platform
(e.g. https://sanskrit.inria.fr/index.en.html) and does not require any installation, however,
HTTP requests are made for every task resulting in a larger delay.


2. Using a local installation

**Installation Instructions: https://sanskrit.inria.fr/manual.html#installation.**

This mode requires a local installation of The Heritage Platform. As
a result, it is considerably faster in obtaining results.


To use Heritage.py in a project,

.. code-block:: python

    import heritage

Credits
=======

This package was created with Cookiecutter_ and the `hrishikeshrt/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`hrishikeshrt/cookiecutter-pypackage`: https://github.com/hrishikeshrt/cookiecutter-pypackage
