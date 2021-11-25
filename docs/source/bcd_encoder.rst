===========
BCD Encoder
===========

The BCD (Binary-Coded Decimal) encoder is a combinatorial circuit that takes an ``N``-bit binary input, ``i_bin``, and converts it to a BCD value,
``o_bcd``, that is ``N + ceil{(N-4)/3} + 1`` bits long. It implements the conversion using the
`double dabble <https://en.wikipedia.org/wiki/Double_dabble>`_ algorithm.

Parameters
----------
- ``N`` number of bits in binary input

Ports
-----
- ``i_bin`` input binary value
- ``o_bcd`` output BCD value

Source Code
-----------
.. literalinclude:: ../../libsv/coders/bcd_encoder.sv
    :language: systemverilog
    :linenos:
    :caption: bcd_encoder.sv
