==============
Binary Counter
==============

This module implements a parameterized binary counter with an active-low asynchronous reset.

With every clock rising, the counter's output ``q`` is incremented by 1. And with an 
assertion of the active-low reset, ``aresetn``, ``q`` is set to 0.

Parameters
----------
- ``N`` number of bits

Inputs/Outputs
--------------
- ``clk`` clock
- ``aresetn`` asynchoronous active-low reset
- ``q`` count (N bits)

Implementation
--------------
.. literalinclude:: ../../openhdl/counters/binary_counter.sv
    :language: systemverilog
    :caption: binary_counter.sv

Block Diagram
-------------
.. figure:: svg/binary_counter.svg
    :align: center
    :width: 100 %

    binary_counter.sv
