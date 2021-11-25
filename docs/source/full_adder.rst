==========
Full Adder
==========

A full adder. Takes three inputs, ``i_a``, ``i_b``, and ``i_carry``, and adds them together to generate a sum output, ``o_sum``, 
and a carry bit output, ``o_carry``.

Ports
-----
- ``i_a`` input a
- ``i_b`` input b
- ``i_carry`` input carry
- ``o_sum`` output sum
- ``o_carry`` output carry

Source Code
-----------
.. literalinclude:: ../../libsv/math/full_adder.sv
    :language: systemverilog
    :linenos:
    :caption: full_adder.sv
