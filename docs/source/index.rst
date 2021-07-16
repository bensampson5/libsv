.. OpenHDL documentation master file, created by
   sphinx-quickstart on Wed Dec 30 22:02:09 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
.. _Cocotb: https://github.com/cocotb/cocotb
.. _Docker: https://www.docker.com/
.. _GTKWave: http://gtkwave.sourceforge.net/
.. _pytest: https://github.com/pytest-dev/pytest
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _Verible: https://github.com/google/verible
.. _Verilator: https://github.com/verilator/verilator

Welcome to OpenHDL's documentation!
===================================

OpenHDL is a library of open source, parameterized digital logic IP. While other similar libraries do exist,
OpenHDL is unique in that it takes advantage of open-source, state-of-the-art development best practices and tools from
across the software and digital design community:

* Python-based, integrated with pytest_, automated testbenches using Cocotb_ + Verilator_ for easy-to-use, fast logic simulation
* All testbenches output waveform files in FST format for viewing with GTKWave_
* `Extensive documention <https://openhdl.readthedocs.io/en/latest/>`_ using Sphinx_ that includes circuit schematics for each module
* Automated formatting and lint checks using Verible_
* `Continuous integration (CI) workflows <https://github.com/bensampson5/openhdl/actions>_`] integrated with Docker_
* `OpenHDL docker images <https://hub.docker.com/repository/docker/bensampson5/openhdl>`_ published to `Docker Hub <https://hub.docker.com/>`_

`Click here to go to OpenHDL's GitHub repository <https://github.com/bensampson5/openhdl>`_

.. toctree::
   :maxdepth: 1
   :caption: Table of Contents:

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
