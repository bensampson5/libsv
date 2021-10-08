===========
BCD Encoder
===========

The BCD (Binary-Coded Decimal) encoder takes an ``N``-bit binary input ``i_bin`` and converts it to a BCD value, ``o_bcd`` that
is ``N + (N-4)/3 + 1`` bits long. It implements the conversion using the `double dabble <https://en.wikipedia.org/wiki/Double_dabble>`_ algorithm.

Parameters
----------
- ``N`` number of bits in binary input

Inputs/Outputs
--------------
- ``i_bin`` input binary value
- ``o_bcd`` output BCD value

Implementation
--------------
.. literalinclude:: ../../src/encode_decode/bcd_encoder/bcd_encoder.sv
    :language: systemverilog
    :caption: bcd_encoder.sv

Block Diagram
-------------

.. figure:: svg/bcd_encoder.svg
    :align: center
    :width: 100 %

    bcd_encoder.sv