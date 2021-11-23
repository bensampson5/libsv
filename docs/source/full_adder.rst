==========
Full Adder
==========

A full adder. Takes three inputs, ``i_a``, ``i_b``, and ``i_carry``, and adds them together to generate a sum output, ``o_sum``, 
and a carry bit output, ``o_carry``.

Inputs/Outputs
--------------
- ``i_a`` input a
- ``i_b`` input b
- ``i_carry`` input carry
- ``o_sum`` output sum
- ``o_carry`` output carry

Implementation
--------------
.. literalinclude:: ../../libsv/math/full_adder.sv
    :language: systemverilog
    :caption: full_adder.sv

Block Diagram
-------------

.. figure:: circuit_diagrams/full_adder.svg
    :align: center
    :width: 100 %

    full_adder.sv