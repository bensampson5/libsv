======
Rotate
======

The rotate module is a combinatorial block that implements a bit-wise left rotation of the
given input data, ``i_data``, by the amount, ``i_amt``. For example, an ``i_data`` of 
``0b10010`` with an ``i_amt`` of ``0b001`` would result in an ``o_data`` of ``0b00101``.

Parameters
----------
- ``DATA_WIDTH`` : data width in bits

Ports
-----
- ``i_data`` input data
- ``i_amt`` amount to rotate
- ``o_data`` output data (rotated version of input)

Source Code
-----------
.. literalinclude:: ../../libsv/bit_ops/rotate.sv
    :language: systemverilog
    :linenos:
    :caption: rotate.sv
