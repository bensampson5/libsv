===========
One-Hot Mux
===========

TBD

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
.. literalinclude:: ../../src/base/mux/onehot_mux.sv
    :language: systemverilog
    :caption: onehot_mux.sv

Block Diagram
-------------

Not available.