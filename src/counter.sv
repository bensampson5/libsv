// Author: Ben Sampson

module counter #(parameter N = 8)
(
    input  logic        clk,
    input  logic        aresetn,
    output logic[N-1:0] q
);

    always @ (posedge clk or negedge aresetn)
        if (!aresetn)
            q <= 0;
        else
            q <= q + 1;

endmodule