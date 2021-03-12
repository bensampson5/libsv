module mux #(
    parameter N  /* verilator public_flat_rd */ = 2
) (
    input  logic [1:0] in,
    input  logic       sel,
    output logic       out
);

  always_comb begin : blockName
    out = sel ? in[0] : in[1];
  end

endmodule
