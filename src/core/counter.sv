/** \file counter.sv
 *  \brief This module implements a parameterized counter with an active-low asynchronous reset.
 *  
 *  With every clock rising, the counter's output ``q`` is incremented by 1. And with an 
 *  assertion of the active-low reset, ``aresetn``, ``q`` is set to 0.
 *
 *  \param N number of bits
 *  \param[in] clk clock
 *  \param[in] aresetn asynchoronous active-low reset
 *  \param[out] q count
 *
 *  \snippet this module
 */

//! [module]
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

endmodule
//! [module]