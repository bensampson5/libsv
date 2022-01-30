================
Priority Encoder
================

The Priority Encoder is a parameterized combinatorial implementation that takes input data,
``i_data``, and outputs a binary priority-encoded output, ``o_data``, where the least significant bit
(bit 0) is the highest priority bit and the most significant bit (bit ``DATA_WIDTH-1``) is the lowest
priority bit. For example, the input ``0b1001`` would result in the output ``0b00`` with the output
valid signal being ``1``. Because the input can be all zeros, it's possible the output is not valid
which is provided by the ``o_valid`` signal.

Parameters
----------
- ``DATA_WIDTH`` : data width in bits

Ports
-----
- ``i_data`` : input data
- ``o_data`` : binary priority-encoded output data
- ``o_valid`` : valid output

Source Code
-----------
.. literalinclude:: ../../libsv/coders/priority_encoder.sv
    :language: systemverilog
    :linenos:
    :caption: priority_encoder.sv
