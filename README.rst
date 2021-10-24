LibSV
=====

Welcome to LibSV! `Click here to go to LibSV’s
documentation <https://libsv.readthedocs.io/en/latest/>`_.

About
-----

LibSV is a library of open source, parameterized digital logic IP
written in SystemVerilog. While other similar libraries do exist, LibSV
is unique in that it takes advantage of open-source, state-of-the-art
development best practices and tools from across the software and
digital design community:

* Python-based, integrated with `pytest <https://github.com/pytest-dev/pytest>`_, automated testbenches using
  `Cocotb <https://github.com/cocotb/cocotb>`_ + `Verilator <https://github.com/verilator/verilator>`_ for 
  easy-to-use, fast logic simulation
* All testbenches output waveform files in FST format for viewing with `GTKWave <http://gtkwave.sourceforge.net/>`_
* `Extensive documention <https://libsv.readthedocs.io/en/latest/>`_ using `Sphinx <https://www.sphinx-doc.org/en/master/>`_
  that includes circuit schematics for each module
* Automated formatting and lint checks using `Verible <https://github.com/google/verible>`_
* `Continuous integration (CI) workflows <https://github.com/bensampson5/libsv/actions>`_ integrated with 
  `Docker <https://www.docker.com/>`_
* `LibSV docker images <https://hub.docker.com/repository/docker/bensampson5/libsv>`_ published to
  `Docker Hub <https://hub.docker.com/>`_

Getting Started
---------------

The easiest way to get started with LibSV is with the publicly available
`LibSV docker images on Docker Hub <https://hub.docker.com/repository/docker/bensampson5/libsv>`__.
To use an LibSV docker image, first you’ll need to install `Docker <https://www.docker.com/get-started>`__, 
if you don’t already have it.

Running Tests
-------------

To run LibSV tests, first, pull the latest LibSV docker image:

.. code:: bash

   docker build --pull -f Dockerfile.dev \
       --build-arg UID=$(id -u) \
       --build-arg GID=$(id -g) \
       -t libsv .

Then, start a new docker container using the LibSV image and mount the
project root folder to the container:

.. code:: bash

   docker run --rm -it -v $(pwd):/code libsv

Finally, within the Docker container, run ``pytest`` - That’s it!

.. code:: bash

   pytest

Each test generates an associated ``.fst`` waveform file that is written out to the ``build/`` directory that can be viewed using
`GTKWave <http://gtkwave.sourceforge.net/>`__.
