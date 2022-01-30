===========
One-hot Mux
===========

A parameterized implementation of a one-hot mux. Takes ``PORTS`` input ports each of width 
``DATA_WIDTH`` as a concatenated input vector, ``i_data``, and using the one-hot select input,
``i_select``, muxes the selected input port to the output, ``o_data``.

Parameters
----------
- ``PORTS`` number of input ports of each ``DATA_WIDTH`` bits
- ``DATA_WIDTH`` data width in bits per input port

Ports
-----
- ``i_data`` concatenated input vector (``PORTS*DATA_WIDTH`` bits)
- ``i_select`` select (``PORTS`` bits)
- ``o_data`` output vector (``DATA_WIDTH`` bits)

Source Code
-----------
.. literalinclude:: ../../libsv/muxes/onehot_mux.sv
    :language: systemverilog
    :linenos:
    :caption: onehot_mux.sv
