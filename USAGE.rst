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

Detailed examples
=================

The :class:`heritage.heritage.HeritagePlatform` class is the main entry point.
It understands both the HTTP interface exposed by sanskrit.inria.fr and the
local binaries provided by the upstream project.

Create a client
---------------

.. code-block:: python

    import os
    from heritage import HeritagePlatform

    # Default behaviour: talks to the INRIA mirror
    web_platform = HeritagePlatform(method="web")

    # Use a local checkout for offline operation
    shell_platform = HeritagePlatform(
        base_dir=os.path.expanduser("~/git/Heritage_Platform"),
        method="shell",
    )

If the executable scripts are missing under ``<base_dir>/ML``, shell mode is
automatically downgraded to web mode and a warning is logged.

Morphological analysis
----------------------

``get_analysis`` returns every solution offered by the Reader Companion for a
piece of Sanskrit input. Each solution contains the original word text and one
or more possible analyses.

.. code-block:: python

    analyses = web_platform.get_analysis("रामः वनं गच्छति", sentence=True)
    first_solution = analyses[1]
    first_word = first_solution["words"][0][0]

    assert first_word["root"] == "राम"
    assert first_word["analyses"][0] == ['pr', 'mas', 'sg', 'nom']

Dependency Roles
----------------

To obtain semantic roles from the Reader Assistant:

.. code-block:: python

    roles = web_platform.get_parse("रामः वनं गच्छति", solution_id=1)
    for role in roles:
        print(role["text"], role["roles"])

Tables
------

Declensions and conjugations are available through the Grammarian utilities.

.. code-block:: python

    declensions = web_platform.get_declensions("राम", gender="m")
    heritage.set_font("roma")  # request IAST output instead of Devanagari

    conjugations = web_platform.get_conjugations("भू", gana="bhwaadi")

Advanced helpers
----------------

* ``heritage.utils.devanagari_to_velthuis`` -- convert input to Velthuis.
* ``heritage.utils.build_query_string`` -- produce QUERY_STRING values when
  calling the CGI scripts manually.
* ``HeritagePlatform.set_lexicon`` -- toggle between Monier-Williams (``MW``)
  and the Heritage dictionary (``SH``).

Structured results
------------------

All high-level helpers return dataclasses defined in :mod:`heritage.models`
when ``structured=True`` (the default). For example,
:class:`heritage.models.SolutionAnalysis` groups every
:class:`heritage.models.WordAnalysis` and keeps the original parser options so
you can revisit a solution later. Convert dataclasses to plain dictionaries via
``dataclasses.asdict`` or the ``heritage.cli`` helpers.

HTTP retries and timeouts
-------------------------

Web mode automatically retries transient failures and decodes responses using
UTF-8. You can tune the behaviour when constructing the platform:

.. code-block:: python

    heritage = HeritagePlatform(
        method="web",
        request_timeout=5,    # seconds per attempt
        request_attempts=4,   # exponential-backoff retries
    )

This configuration is respected by every helper that issues HTTP requests and
is also used when fetching dictionary entries.

Command line interface
----------------------

The ``heritage`` CLI exposes the same capabilities for quick experimentation:

.. code-block:: console

    $ heritage conjugation गम् --gana bhwaadi
    लट्
      परस्मैपदम्
        प्रथमपुरुषः	गच्छति
        ...

Pass ``--json`` to get machine-readable output or ``--method shell`` to target a
local installation.

Troubleshooting
---------------

* Enable logging::

  .. code-block:: python

      import logging
      logging.basicConfig(level=logging.INFO)

* Intermittent HTTP errors trigger exponential backoff and retries.
* Shell mode uses a timeout; long-running executables log an error and return
  ``None`` instead of raw HTML when the underlying CGI scripts do not respond
  in time.
