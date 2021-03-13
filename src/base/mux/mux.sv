`include "functions.svh"

module mux #(
    parameter DW  /* verilator public_flat_rd */ = 1,  // width of data inputs
    parameter N  /* verilator public_flat_rd */  = 2  // number of inputs
) (
    input  logic [   N-1:0] sel,  // select vector
    input  logic [N*DW-1:0] in,  // concatenated input {..,in1[DW-1:0],in0[DW-1:0]
    output logic [  DW-1:0] out  // output
);

  integer i;
  always_comb begin
    out[DW-1:0] = 'b0;
    for (i = 0; i < N; i = i + 1) out[DW-1:0] |= {(DW) {sel[i]}} & in[((i+1)*DW-1)-:DW];
  end

endmodule  // mux
