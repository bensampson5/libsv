===========
One-Hot Mux
===========

A parameterized implementation of a one-hot mux. Takes ``N`` inputs each of width ``DW`` as a concatenated input vector ``in``
and given a one-hot ``sel`` input, routes the selected input vector to the output vector ``out``.

Parameters
----------
- ``DW`` data width (per input vector)
- ``N`` number of inputs

Inputs/Outputs
--------------
- ``sel`` select (N bits)
- ``in`` concatenated input vector (DW*N bits)
- ``out`` output vector (DW bits)

Implementation
--------------
.. literalinclude:: ../../src/core/mux/onehot_mux.sv
    :language: systemverilog
    :caption: onehot_mux.sv

Block Diagram
-------------

Not available.