.. _skid-buffer:

===========
Skid Buffer
===========

A skid buffer is used to break apart a combinatorial path between a sender and receiver interface by registering
the data and handshake signals. The skid buffer uses two buffer entries, a main buffer and a "skid" buffer, that
allows it to maintain the full throughput, thus pipelining the data path. Because there is a one clock cycle 
latency through the skid buffer for backpressuring the sender if it is backpressured by the receiver, the "skid"
buffer is needed to absorb one extra transaction from the sender, before it can actually backpressure the sender.
Skid buffers are commonly used for pipelining and resolving timing issues by breaking long combinatorial paths
between a sender and receiver. Because there are only two buffer registers, it is also a very lightweight
solution.

This skid buffer implementation also provides two additional output status signals, ``o_accept`` and ``o_transmit``,
which indicate when a transaction is successfully accepted from the input interface or successfully transmitted to
the output interface. These two additional signals are provided so that a parent module can keep track of 
when the skid buffer is accepting or transmitting data. For example, this could be useful if the parent module
needs that information for some of its own control logic or if it wants to keep track of how many transcations
have been accepted and transmitted by the skid buffer.


Parameters
----------
- ``DATA_WIDTH`` : data width in bits

Ports
-----
- ``i_clock`` : input clock
- ``i_aresetn`` : asynchronous active-low reset
- ``i_clear`` : synchronous clear
- ``i_data`` : input data
- ``i_input_valid`` : valid signal from input interface. Used with o_input_ready to handshake on input interface
- ``i_output_ready`` : ready signal from output interface. Used with o_output_valid to handshake on output interface
- ``o_data`` : output data
- ``o_output_valid`` : valid signal from output interface. Used with i_output_ready to handshake on output interface
- ``o_input_ready`` : ready signal from input interface. Used with i_input_valid to handshake on input interface
- ``o_accept`` : accept status signal that indicates whenever input data is accepted by the skid buffer
- ``o_transmit`` : transmit status signal that indicates whenever output data is transmitted by the skid buffer

Source Code
-----------
.. literalinclude:: ../../libsv/fifos/skid_buffer.sv
    :language: systemverilog
    :linenos:
    :caption: skid_buffer.sv
