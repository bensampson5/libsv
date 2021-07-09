module onehot_mux #(
    parameter DW  /* verilator public_flat_rd */ = 8,
    parameter N  /* verilator public_flat_rd */  = 4
) (
    input  logic [   N-1:0] sel,
    input  logic [N*DW-1:0] i,
    output logic [  DW-1:0] o
);

  integer j;
  always_comb begin
    o[DW-1:0] = 'b0;
    for (j = 0; j < N; j = j + 1) o[DW-1:0] |= {(DW) {sel[j]}} & i[((j+1)*DW-1)-:DW];
  end

endmodule  // onehot_mux
