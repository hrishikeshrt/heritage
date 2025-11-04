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

Quickstart
==========

.. code-block:: python

    from heritage import HeritagePlatform

    # Use the INRIA mirror (default behaviour)
    heritage = HeritagePlatform(method="web")

    analyses = heritage.get_analysis("रामः वनं गच्छति", sentence=True)
    solution = analyses[1]  # solutions are keyed by solution_id
    first_word = solution["words"][0][0]

    print(first_word["text"])        # -> 'रामः'
    print(first_word["root"])        # -> 'राम'
    print(first_word["analyses"])    # -> [['pr', 'mas', 'sg', 'nom']]

    heritage.set_lexicon("SH")       # Switch to the Heritage dictionary
    declensions = heritage.get_declensions("राम", gender="m")

Choosing a data source
======================

Web mirror (default)
    Nothing to install. Calls ``https://sanskrit.inria.fr`` (or any mirror you
    configure) for every request, so latency depends on network access.

Local installation
    Clone the upstream ``Heritage_Platform`` repository, compile the tools, and
    point Heritage.py at that checkout::

        from pathlib import Path
        heritage = HeritagePlatform(
            base_dir=Path("~/git/Heritage_Platform").expanduser(),
            method="shell",
        )

    Shell mode is faster and works offline, but requires the compiled binaries
    to be available in ``<base_dir>/ML``. If the directory is missing the helper
    falls back to web mode automatically.

Core API at a glance
====================

``HeritagePlatform.get_analysis(text, sentence=True, unsandhied=False, meta=False)``
    Run the Reader Companion and receive structured morphological analyses.

``HeritagePlatform.get_parse(text, solution_id=None, ...)``
    Fetch semantic roles for a sentence from the Reader Assistant.

``HeritagePlatform.get_declensions(word, gender, headers=True)``
    Retrieve declension tables from the Grammarian.

``HeritagePlatform.get_conjugations(word, gana, lexicon=None)``
    Request conjugation tables (parsing into structured data is planned).

``HeritagePlatform.search_lexicon(word, lexicon=None)``
    Query the dictionary interface (returns raw HTML for now).

``heritage.utils.devanagari_to_velthuis(text)``
    Convert Devanagari script to the Velthuis scheme expected upstream.

``heritage.utils.build_query_string(options)``
    Assemble query strings for direct Heritage CGI calls.

Network configuration
=====================

The wrapper exposes simple knobs for HTTP behaviour when you rely on the online
mirror.

.. code-block:: python

    heritage = HeritagePlatform(
        method="web",
        request_timeout=5,      # seconds per HTTP request
        request_attempts=4,     # number of retries before failing
    )

Requests are retried with exponential backoff and decoded as UTF-8 even when
the server omits a charset header, preventing garbled Sanskrit text (mojibake)
in the parsed output.

Troubleshooting
===============

* Enable logging to inspect low-level behaviour::

      import logging
      logging.basicConfig(level=logging.INFO)

* ``set_method("shell")`` falls back to web mode automatically when the local
  installation is missing.
* Network calls use retries with exponential backoff; expect short delays on
  transient failures.
* The CLI entry point currently prints a placeholder message. Contributions to
  build a feature-rich CLI are welcome.

Credits
=======

This package was created with Cookiecutter_ and the `hrishikeshrt/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`hrishikeshrt/cookiecutter-pypackage`: https://github.com/hrishikeshrt/cookiecutter-pypackage
