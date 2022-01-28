.. image:: https://raw.githubusercontent.com/bensampson5/libsv/main/docs/source/_static/libsv_logo.svg
   :align: center
   :height: 150
   :alt: LibSV

------------------------------------------------------------------------------------------------------------------------

.. image:: https://img.shields.io/pypi/v/libsv
   :target: https://pypi.org/project/libsv/
   :alt: PyPI

.. image:: https://github.com/bensampson5/libsv/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/bensampson5/libsv/actions/workflows/ci.yml

.. image:: https://readthedocs.org/projects/libsv/badge/?version=latest
   :target: https://libsv.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

Welcome to LibSV! `Click here to go to LibSV’s
documentation <https://libsv.readthedocs.io/en/latest/>`_.

LibSV is an open source, parameterized SystemVerilog digital hardware IP library.
While similar libraries may already exist, LibSV is unique in that it takes advantage
of open-source, state-of-the-art development best practices and tools from across the
software and digital design community, including:

* Trivial installation. `LibSV is hosted on PyPI <https://pypi.org/project/libsv/>`_ and can easily be installed using 
  `pip <https://pip.pypa.io/en/stable/>`_ or whichever Python package manager of your choice.
* Easy-to-use. Simply add ```include "libsv/<path>/<to>/<module>.sv"`` to where you want to use a LibSV module and then add the
  ``site-packages/`` folder, where LibSV was installed, to the include path when building your project.
* Automated testbenches, written in Python, that use `pytest <https://github.com/pytest-dev/pytest>`_ to run
  `Cocotb <https://github.com/cocotb/cocotb>`_ + `Verilator <https://github.com/verilator/verilator>`_ under the hood for 
  simple and fast logic simulation
* All testbenches output waveform files in FST format for viewing with `GTKWave <http://gtkwave.sourceforge.net/>`_
* `Extensive documention <https://libsv.readthedocs.io/en/latest/>`_ using `Sphinx <https://www.sphinx-doc.org/en/master/>`_
* Each module is tested for synthesizeability using `yosys <https://github.com/YosysHQ/yosys>`_
* Automated formatting and lint checks using `Verible <https://github.com/google/verible>`_
* `Continuous integration (CI) workflows <https://github.com/bensampson5/libsv/actions>`_ integrated with 
  `Docker <https://www.docker.com/>`_
* `LibSV Docker images <https://hub.docker.com/repository/docker/bensampson5/libsv>`_ published to
  `Docker Hub <https://hub.docker.com/>`_

Getting Started
---------------

LibSV is very easy to use. First, install the ``libsv`` package from PyPI:

.. code-block:: bash

  pip install libsv

We recommend using a Python virtual environment so that the installation is project-specific and
isolated from the rest of your system.

Then add the ``site-packages/`` folder, where LibSV was just installed, to your include path when building your
project so that your design tools can find LibSV.

Finally, at the top of your design file where you want to use LibSV modules, for each module you want to use, add:

.. code-block:: SystemVerilog

  `include "libsv/<path>/<to>/<module>.sv"

Running Testbenches
-------------------

Running the LibSV testbenches require `Cocotb <https://github.com/cocotb/cocotb>`_, 
`Verilator <https://github.com/verilator/verilator>`_, and a number of other dependencies to be installed.
Instead of trying to install everything manually on your machine, the easier and recommended way to run the
LibSV testbenches is to use the pre-built 
`LibSV Docker images on Docker Hub <https://hub.docker.com/repository/docker/bensampson5/libsv>`__ that have the
complete set of LibSV developer tools already installed.

To use a LibSV Docker image, first you’ll need to install `Docker <https://www.docker.com/get-started>`__, 
if you don’t already have it.

Next, pull the latest LibSV Docker image:

.. code-block:: bash

  docker build --pull -f Dockerfile.dev \
    --build-arg UID=$(id -u) \
    --build-arg GID=$(id -g) \
    -t libsv .

Then, start a new Docker container using the LibSV image and mount the project folder to the container:

.. code-block:: bash

  docker run --rm -it -v $(pwd):/code libsv

Finally, within the Docker container, run ``pytest``:

.. code-block:: bash

  pytest

This will run all the LibSV testbenches for the entire library (*Warning: This may take a while!*).

Instead, to list all the available LibSV testbenches, run:

.. code-block:: bash

  pytest --co

Then, you can run an individual or subset of testbenches using the ``-k`` flag which will only run tests which
match the given substring expression:

.. code-block:: bash

  pytest -k EXPRESSION

Each testbench generates an associated ``.fst`` waveform file that is written to the ``build/`` directory and can be
viewed using `GTKWave <http://gtkwave.sourceforge.net/>`_.

Bugs/Feature Requests
---------------------

Please use `LibSV's GitHub issue tracker <https://github.com/bensampson5/libsv/issues>`_ to submit bugs or request features.

Contributing
------------

Contributions are much welcomed and appreciated! Take a look at the 
`Contributing <https://libsv.readthedocs.io/en/latest/contributing.html>`_ page to get started.

License
-------

Distributed under the terms of the `MIT <https://github.com/bensampson5/libsv/blob/main/LICENSE>`_ license, LibSV is free
and open source software.
