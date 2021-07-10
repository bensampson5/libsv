module counter #(
    parameter integer N  /* verilator public_flat_rd */ = 8
) (
    input  logic         clk,
    input  logic         aresetn,
    output logic [N-1:0] q
);

  always_ff @(posedge clk or negedge aresetn)
    if (!aresetn) q <= 0;
    else q <= q + 1;

endmodule
