==========
Half Adder
==========

A half adder. Takes two inputs, ``i_a`` and ``i_b``, and adds them together to generate a sum output, ``o_sum``, 
and a carry bit output, ``o_carry``.

Ports
-----
- ``i_a`` input a
- ``i_b`` input b
- ``o_sum`` output sum
- ``o_carry`` output carry

Source Code
-----------
.. literalinclude:: ../../libsv/math/half_adder.sv
    :language: systemverilog
    :linenos:
    :caption: half_adder.sv
