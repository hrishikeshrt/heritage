.. highlight:: shell

============
Installation
============


Stable release
--------------

To install Heritage.py, run this command in your terminal:

.. code-block:: console

    $ pip install heritage

This is the preferred method to install Heritage.py, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for Heritage.py can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/hrishikeshrt/heritage

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/hrishikeshrt/heritage/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


Editable installs and development tooling
-----------------------------------------

While working on the wrapper itself it can be convenient to install it in
editable mode and pull in the additional development utilities:

.. code-block:: console

    $ pip install -e .
    $ pip install -r requirements_dev.txt

This setup keeps your virtual environment in sync with the source tree and
exposes linting and documentation dependencies.


Using a local Heritage Platform checkout
----------------------------------------

The Python wrapper can invoke the CGI-style binaries from the upstream
``Heritage_Platform`` repository. This makes lookups faster and removes the
network dependency.

1. Follow the `official installation guide`_ to build the tools.
2. Ensure executables such as ``./ML/reader`` are present and runnable.
3. Point Heritage.py at the checkout::

.. code-block:: python

    import os
    from heritage import HeritagePlatform

    platform = HeritagePlatform(
        base_dir=os.path.expanduser("~/git/Heritage_Platform"),
        method="shell",
    )

4. Optional: switch back to the web mirror by calling ``platform.set_method("web")``.

Heritage.py validates ``<base_dir>/ML`` and falls back to HTTP mode if the
directory is missing, logging a warning in the process.

.. _official installation guide: https://sanskrit.inria.fr/manual.html#installation


.. _Github repo: https://github.com/hrishikeshrt/heritage
.. _tarball: https://github.com/hrishikeshrt/heritage/tarball/master
