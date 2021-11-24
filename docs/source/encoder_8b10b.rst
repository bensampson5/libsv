==============
8B/10B Encoder
==============

8B/10B encoding is a line code that maps 8-bit words to 10-bit symbols to achieve DC-balance and bounded
disparity, while at the same time provide enough state changes to allow reasonable clock recovery. This 
8B/10B encoder implementation is a combinatorial circuit that takes an 8-bit binary input, ``i_8b``, and
outputs a 10-bit binary value, ``o_10b``, according to 
`IBM's 8B/10B implementation <https://en.wikipedia.org/wiki/8b/10b_encoding#IBM_implementation>`_.

The input running disparity (RD) is required via the ``i_rd`` input where ``0`` equals an input RD of -1
and ``1`` equals an input RD of +1. Also, the ``i_ctrl`` input is used to select whether the encoder
outputs a data symbol (D.x.y) when ``i_ctrl`` = ``0``, or a control symbol (K.x.y) when ``i_ctrl`` =
``0``. Along with the 10b encoded output symbol, this module provides an ``o_rd`` output signal which
represents the output running disparity after encoding, where ``0`` equals an output RD of -1 and ``1``
equals an output RD of +1.

In almost all use-cases, the user is required to keep track of the running disparity over a given 
data stream being encoded but this feature is not handled by this module as it is a purely combinatorial
implementation. Instead, this is left to the user to implement in the parent module that instantiates
this module although the ``o_rd`` output signal is provided for convenience. For example, a simple
implementation that would maintain the running disparity over an input data stream would be registering
``o_rd`` and then feeding the output of that register back into this module as ``i_rd``.

IBM's 8B/10B implementation is defined by partitioning the coder into 5B/6B and 3B/4B subordinate coders
as described in the tables below. Using these tables, a given input 8-bit value, ``HGFEDCBA``, along
with the input running disparity and a control symbol select bit, can be encoded to its corresponding
unique 10-bit value, ``jhgfiedcba``.


.. table:: 5B/6B Coding Table
    :header-alignment: cccccccc
    :column-alignment: cccccccc

    +--------------+---------+----------+----------------+---------+----------+
    |     Input    | RD = −1 | RD = +1  |      Input     | RD = −1 | RD = +1  |
    +======+=======+=========+==========+========+=======+=========+==========+
    | Code | EDCBA |       abcdei       |  Code  | EDCBA |       abcdei       |
    +------+-------+---------+----------+--------+-------+---------+----------+
    | D.00 | 00000 |  100111 |  011000  |  D.16  | 10000 |  011011 |  100100  |
    +------+-------+---------+----------+--------+-------+---------+----------+
    | D.01 | 00001 |  011101 |  100010  |  D.17  | 10001 |       100011       |
    +------+-------+---------+----------+--------+-------+--------------------+
    | D.02 | 00010 |  101101 |  010010  |  D.18  | 10010 |       010011       |
    +------+-------+---------+----------+--------+-------+--------------------+
    | D.03 | 00011 |       110001       |  D.19  | 10011 |       110010       |
    +------+-------+---------+----------+--------+-------+--------------------+
    | D.04 | 00100 |  110101 |  001010  |  D.20  | 10100 |       001011       |
    +------+-------+---------+----------+--------+-------+--------------------+
    | D.05 | 00101 |       101001       |  D.21  | 10101 |       101010       |
    +------+-------+--------------------+--------+-------+--------------------+
    | D.06 | 00110 |       011001       |  D.22  | 10110 |       011010       |
    +------+-------+---------+----------+--------+-------+---------+----------+
    | D.07 | 00111 |  111000 |  000111  | D.23 † | 10111 |  111010 |  000101  |
    +------+-------+---------+----------+--------+-------+---------+----------+
    | D.08 | 01000 |  111001 |  000110  |  D.24  | 11000 |  110011 |  001100  |
    +------+-------+---------+----------+--------+-------+---------+----------+
    | D.09 | 01001 |       100101       |  D.25  | 11001 |       100110       |
    +------+-------+--------------------+--------+-------+--------------------+
    | D.10 | 01010 |       010101       |  D.26  | 11010 |       010110       |
    +------+-------+--------------------+--------+-------+---------+----------+
    | D.11 | 01011 |       110100       | D.27 † | 11011 |  110110 |  001001  |
    +------+-------+--------------------+--------+-------+---------+----------+
    | D.12 | 01100 |       001101       |  D.28  | 11100 |       001110       |
    +------+-------+--------------------+--------+-------+---------+----------+
    | D.13 | 01101 |       101100       | D.29 † | 11101 |  101110 |  010001  |
    +------+-------+--------------------+--------+-------+---------+----------+
    | D.14 | 01110 |       011100       | D.30 † | 11110 |  011110 |  100001  |
    +------+-------+---------+----------+--------+-------+---------+----------+
    | D.15 | 01111 |  010111 |  101000  |  D.31  | 11111 |  101011 |  010100  |
    +------+-------+---------+----------+--------+-------+---------+----------+
    |                                   | K.28 ‡ | 11100 |  001111 |  110000  |
    +-----------------------------------+--------+-------+---------+----------+
    
† *also used for the 5b/6b code of K.x.7*

‡ *exclusively used for the 5b/6b code of K.28.y*


.. table:: 3B/4B Coding Table
    :header-alignment: cccccccc
    :column-alignment: cccccccc

    +----------------+---------+----------+---------------+---------+----------+
    |      Input     | RD = −1 | RD = +1  |     Input     | RD = −1 | RD = +1  |
    +----------+-----+---------+----------+---------+-----+---------+----------+
    |   Code   | HGF |        fghj        |   Code  | HGF |        fghj        |
    +==========+=====+=========+==========+=========+=====+=========+==========+
    | D.x.0    | 000 |   1011  |   0100   | K.x.0   | 000 |   1011  |   0100   |
    +----------+-----+---------+----------+---------+-----+---------+----------+
    | D.x.1    | 001 |        1001        | K.x.1 ‡ | 001 |   0110  |   1001   |
    +----------+-----+--------------------+---------+-----+---------+----------+
    | D.x.2    | 010 |        0101        | K.x.2   | 010 |   1010  |   0101   |
    +----------+-----+---------+----------+---------+-----+---------+----------+
    | D.x.3    | 011 |   1100  |   0011   | K.x.3   | 011 |   1100  |   0011   |
    +----------+-----+---------+----------+---------+-----+---------+----------+
    | D.x.4    | 100 |   1101  |   0010   | K.x.4   | 100 |   1101  |   0010   |
    +----------+-----+---------+----------+---------+-----+---------+----------+
    | D.x.5    | 101 |        1010        | K.x.5 ‡ | 101 |   0101  |   1010   |
    +----------+-----+--------------------+---------+-----+---------+----------+
    | D.x.6    | 110 |        0110        | K.x.6   | 110 |   1001  |   0110   |
    +----------+-----+---------+----------+---------+-----+---------+----------+
    | D.x.P7 † |     |   1110  |   0001   | K.x.7 ‡ | 111 |   0111  |   1000   |
    +----------+ 111 +---------+----------+---------+-----+---------+----------+
    | D.x.A7 † |     |   0111  |   1000   |                                    |
    +----------+-----+---------+----------+------------------------------------+

† *For D.x.7, either the Primary (D.x.P7), or the Alternate (D.x.A7) encoding must be selected*
*in order to avoid a run of five consecutive 0s or 1s when combined with the preceding 5b/6b code.*
*Sequences of exactly five identical bits are used in comma symbols for synchronization issues.*
*D.x.A7 is used only when:*

    * *RD = −1: for x = 17, 18 and 20*
    * *RD = +1: for x = 11, 13 and 14*

*With x = 23, x = 27, x = 29, and x = 30, the 3b/4b code portion used for control symbols K.x.7 is*
*the same as that for D.x.A7. Any other D.x.A7 code can't be used as it would result in chances for*
*misaligned comma sequences.*

‡ *Only K.28.1, K.28.5, and K.28.7 generate comma symbols, that contain a bit sequence of five 0s or*
*1s. The symbol has the format 110000 01xx or 001111 10xx.*

Parameters
----------
- None

Inputs/Outputs
--------------
- ``i_8b`` input 8-bit binary value (bit-order is ``HGFEDCBA`` where ``A`` is the lsb)
- ``i_rd`` input running disparity (``0`` = -1, ``1`` = +1)
- ``i_ctrl`` input control symbol flag (``0`` = data symbol, ``1`` = control symbol)
- ``o_10b`` output 10-bit binary value (bit-order is ``jhgfiedcba`` where ``a`` is the lsb)
- ``o_rd`` output running disparity (``0`` = -1, ``1`` = +1)

Implementation
--------------
.. literalinclude:: ../../libsv/coders/encoder_8b10b.sv
    :language: systemverilog
    :caption: encoder_8b10b.sv

Block Diagram
-------------

Not available.