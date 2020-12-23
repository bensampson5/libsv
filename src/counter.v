// Author: Ben Sampson

module counter #(parameter N = 8)
(
    input clk,
    output reg[N-1:0] q
);

    always @ (posedge clk)
        q <= q + 1;

endmodule