.. OpenHDL documentation master file, created by
   sphinx-quickstart on Wed Dec 30 22:02:09 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to OpenHDL's documentation!
===================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

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
