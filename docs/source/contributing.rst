Contributing
============

Contributions are much welcomed and appreciated!

.. contents::
   :depth: 2
   :backlinks: none


.. _submitfeedback:

Feature requests and feedback
-----------------------------

We'd like to hear about your propositions and suggestions.  Feel free to
`submit them as issues <https://github.com/bensampson5/libsv/issues>`_ and:

* Explain in detail how they should work.
* Keep the scope as narrow as possible.  This will make it easier to implement.

Or create/join a discussion in the `LibSV discussion page <https://github.com/bensampson5/libsv/discussions>`_.


.. _report_bugs:

Report bugs
-----------

Report bugs for LibSV in the `issue tracker <https://github.com/bensampson5/libsv/issues>`_.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting,
  specifically the Python interpreter version, installed libraries & packages
  (i.e. cocotb, verilator, pytest), and whether or not you're using a LibSV Docker
  image.
* Detailed steps to reproduce the bug.

If you can write a demonstration test that currently fails but should pass
(xfail), that is a very useful commit to make as well, even if you cannot
fix the bug itself.


.. _setting_up_developers_environment

Setting up the LibSV developer's environment
--------------------------------------------

For anything beyond feature requests, reporting bugs, or very simple fixes, it is *strongly* recommended to setup the LibSV
developer's environment. Especially if you plan to write any SystemVerilog source code, write and/or run Python testbenches,
build the html documentation from source, or modify project workflows/tools/configurations.

LibSV provides pre-built Docker images, specifically for this purpose, which are available on 
`LibSV's Docker Hub page <https://hub.docker.com/repository/docker/bensampson5/libsv>`_. If you don't already have 
`Docker <https://www.docker.com/>`_ installed on your machine, you will need to install it by following the instructions
`here <https://docs.docker.com/get-docker/>`_.

Once you have Docker installed you can build and pull the LibSV Docker image by running:

.. code-block:: bash

  docker build --pull -f Dockerfile.dev \
    --build-arg UID=$(id -u) \
    --build-arg GID=$(id -g) \
    -t libsv .

By default, this will pull the LibSV Docker image associated with the ``main`` branch, however you can pull a different branch's
LibSV Docker image by adding the ``BRANCH`` build argument:

.. code-block:: bash

  docker build --pull -f Dockerfile.dev \
    --build-arg UID=$(id -u) \
    --build-arg GID=$(id -g) \
    --build-arg BRANCH=TYPE_BRANCH_NAME_HERE \
    -t libsv .

Then, start a new Docker container using the LibSV image and mount the project folder to the container:

.. code-block:: bash

  docker run --rm -it -v $(pwd):/code libsv


.. _fix_bugs:

Fix bugs
--------

Look through the `issue tracker for bugs <https://github.com/bensampson5/libsv/issues?q=is%3Aissue+is%3Aopen+label%3Abug>`_.

If you're interested in fixing a bug but are unsure about how you can fix it, leave a comment in the specific issue so that
developers can help you find a solution. To indicate that you are going to work on a particular issue, add a comment to that
effect in the issue.


.. _implement_features:

Implement features
------------------

Look through the `issue tracker for enhancements <https://github.com/bensampson5/libsv/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement>`_.

If you're interested in implementing a feature but are unsure about how you can do it, leave a comment in the specific issue
so that developers can help you find a solution. To indicate that you are going to work on a particular feature, add a comment
to that effect in the issue.


.. _write_documentation:

Write documentation
-------------------

LibSV could always use more documentation.  What exactly is needed?

* Online documentation
* Code comments (including both SystemVerilog source files and python testbenches)

You can also edit documentation files directly in the GitHub web interface,
without using a local copy.  This can be convenient for small fixes.

.. note::
    Build the documentation locally by running the following bash command in a LibSV Docker container
    from the top-level project directory:

    .. code-block:: bash

        ./tools/precommit.py --docs

    The built documentation should be available in ``docs/build/html/``.


.. _pull_requests:

Preparing Pull Requests
-----------------------

Pull requests inform the project's core developers about the
changes you want to review and merge.  Pull requests are stored on
`GitHub servers <https://github.com/pytest-dev/pytest/pulls>`_.
Once you send a pull request, we can discuss its potential modifications and
even add more commits to it later on. There's an excellent tutorial on how Pull
Requests work in the
`GitHub Help Center <https://help.github.com/articles/using-pull-requests/>`_.

To prepare a pull request:

#. Fork the repository.
#. As you make changes and before you commit, run the 
   `precommit <https://github.com/bensampson5/libsv/blob/main/tools/precommit.py>`_ script by
   invoking ``./tools/precommit.py`` from the top-level project directory when you're running
   in a LibSV Docker container. To see all precommit script options run: ``./tools/precommit.py --help``.
#. Testbenches are run using either ``pytest`` or ``./tools/precommit.py --test``. This will run all
   LibSV testbenches. To run only a single testbench, we recommend using ``pytest`` with the ``-k`` flag
   
    .. code-block:: bash

        pytest -k TESTBENCH_NAME

#. If you are adding a new SystemVerilog module to the library, you must complete the following checklist:

    * The new SystemVerilog module should be a single ``.sv`` file with a single ``module`` inside that
      is added to the right directory within ``libsv/``. File naming convention is all lower-case and
      underscores (i.e. ``example_module.sv``).
    * The SystemVerilog module should have a corresponding Python testbench that has the same name as
      the SystemVerilog source file with a ``test_`` prefix. (i.e. ``test_example_module.sv``). Similarly
      to before, this testbench must be added to the right directory within ``tests/``. Take a look
      at `existing LibSV testbenches <https://github.com/bensampson5/libsv/tree/main/tests>`_ for examples
      on how to write a testbench for LibSV.
    * Write a testbench that exercises the SystemVerilog module and checks whether the module meets the
      functional specifications.
    * The SystemVerilog module should have a corresponding ``.rst`` documentation file that has the same
      name as the SystemVerilog source file (i.e. ``example_module.rst``). Once again, this documentation
      file must be added to the right directory within ``docs/source/``. Take a look at 
      `existing LibSV docs <https://github.com/bensampson5/libsv/tree/main/docs/source>`_ for examples on 
      how write documentation for LibSV.

#. Unless your change is a trivial or a documentation fix (e.g., a typo or reword of a small section),
   please add yourself as a contributor to the ``AUTHORS`` file, in alphabetical order, so we can credit
   you for your work!
#. Commit and push once the precommit script passes and you are happy with your changes:

    .. code-block:: bash

        git commit -a -m "<commit message>"
        git push -u

#. Finally, submit a pull request through GitHub using this data:

    .. code-block:: text

        head repository: YOUR_GITHUB_USERNAME/libsv
        compare: your-branch-name

        base repository: bensampson5/libsv
        base: main


.. _closing_issues:

Closing Issues
--------------

When a pull request is submitted to fix an issue, add text like ``Closes #ABC`` to the PR description and/or commits (where ``ABC`` is the
issue number). See the
`GitHub docs <https://help.github.com/en/github/managing-your-work-on-github/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword>`_
for more information.