===========
BCD Decoder
===========

The BCD (Binary-Coded Decimal) decoder is a combinatorial circuit takes a ``N`` decimal digit BCD input and converts it to a binary output.
The BCD input , ``i_bcd``, is a ``4*N`` bit wide input vector where each 4 bits represents one decimal digit. The output binary value, ``o_bin``,
is ``3*N + floor{(N+2)/3}`` bits long. It implements the conversion using the reverse `double dabble <https://en.wikipedia.org/wiki/Double_dabble>`_ algorithm.

Parameters
----------
- ``N`` number of digits in BCD input

Inputs/Outputs
--------------
- ``i_bcd`` input BCD value
- ``o_bin`` output binary value

Implementation
--------------
.. literalinclude:: ../../libsv/decoders/bcd_decoder.sv
    :language: systemverilog
    :caption: bcd_decoder.sv

Block Diagram
-------------

.. figure:: circuit_diagramsbcd_decoder.svg
    :align: center
    :width: 100 %

    bcd_decoder.sv