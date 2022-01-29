`ifndef LIBSV_BIT_OPS_ROTATE
`define LIBSV_BIT_OPS_ROTATE

module rotate #(
    parameter int WIDTH  /* verilator public_flat_rd */ = 8
) (
    input  logic [        WIDTH-1:0] i_in,
    input  logic [$clog2(WIDTH)-1:0] i_amt,
    output logic [        WIDTH-1:0] o_out
);

  always_comb begin : rotate
    o_out = '0;
    for (int i = 0; i < WIDTH; ++i) begin
      int rotate_amt = (int'(i_amt) + i) % WIDTH;
      o_out[$bits(i_amt)'(rotate_amt)] = i_in[i];
    end
  end : rotate

endmodule : rotate

`endif /* LIBSV_BIT_OPS_ROTATE */