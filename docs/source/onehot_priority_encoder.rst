.. _one-hot-priority-encoder:

========================
One-hot Priority Encoder
========================

The One-hot Priority Encoder is a parameterized combinatorial implementation that takes input data,
``i_data``, and outputs a one-hot priority-encoded output, ``o_data``, where the least significant bit
(bit 0) is the highest priority bit and the most significant bit (bit ``DATA_WIDTH-1``) is the lowest
priority bit. For example, the input ``0b1001`` would result in the output ``0b0001``.

Parameters
----------
- ``DATA_WIDTH`` : data width in bits

Ports
-----
- ``i_data`` : input data
- ``o_data`` : one-hot priority-encoded output data

Source Code
-----------
.. literalinclude:: ../../libsv/coders/onehot_priority_encoder.sv
    :language: systemverilog
    :linenos:
    :caption: onehot_priority_encoder.sv
