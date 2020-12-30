Counter
=======

This is a new file.

.. code-block:: systemverilog

   module counter
   #(
      parameter N /* verilator public_flat_rd */ = 16
   )
   (
      input logic clk,
      input logic aresetn,
      output logic[N-1:0] q
   );

      always_ff @(posedge clk or negedge aresetn)
         if (!aresetn)
               q <= 0;
         else
               q <= q + 1;