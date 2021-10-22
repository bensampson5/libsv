========
SR Latch
========

This module implements a `SR NOR latch <https://en.wikipedia.org/wiki/Flip-flop_(electronics)#SR_NOR_latch>`_.

While ``s`` (set) and ``r`` (reset) are both low, ``q``  and ``q_n`` are maintained in a constant state, with ``q_n`` being
the complement of ``q``.If ``s`` goes high while ``r`` is held low, then ``q`` is forced high. Similarly, if ``r`` goes high
while ``s`` is held low, then ``q`` is forced low. Having both ``s`` and ``r`` high (``1``) is a restricted combination.

Inputs/Outputs
--------------
- ``s`` set
- ``r`` reset
- ``q`` output
- ``q_n`` complemented output

Implementation
--------------
.. literalinclude:: ../../src/latch/sr_latch/sr_latch.sv
    :language: systemverilog
    :caption: sr_latch.sv

Block Diagram
-------------
.. figure:: svg/sr_latch.svg
    :align: center
    :width: 100 %

    sr_latch.sv
