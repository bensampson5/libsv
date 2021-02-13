=======
Counter
=======

This module implements a parameterized counter with an active-low asynchronous reset.

With every clock rising, the counter's output ``q`` is incremented by 1. And with an 
assertion of the active-low reset, ``aresetn``, ``q`` is set to 0.

Parameters
----------
 - ``N`` number of bits
 - ``clk`` clock
 - ``aresetn`` asynchoronous active-low reset
 - ``q`` count

Implementation
--------------
.. literalinclude:: ../../src/counter/counter.sv
    :language: systemverilog
    :caption: counter.sv

Block Diagram
-------------
.. figure:: svg/counter.svg
    :align: center
    :width: 100 %

    counter.sv
