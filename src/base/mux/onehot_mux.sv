module onehot_mux #(
    parameter DW  /* verilator public_flat_rd */ = 8,
    parameter N  /* verilator public_flat_rd */  = 4
) (
    input  logic [   N-1:0] sel,
    input  logic [N*DW-1:0] in,
    output logic [  DW-1:0] out
);

  integer i;
  always_comb begin
    out[DW-1:0] = 'b0;
    for (i = 0; i < N; i = i + 1) out[DW-1:0] |= {(DW) {sel[i]}} & in[((i+1)*DW-1)-:DW];
  end

endmodule  // onehot_mux
