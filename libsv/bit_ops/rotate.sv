`ifndef LIBSV_BIT_OPS_ROTATE
`define LIBSV_BIT_OPS_ROTATE

module rotate #(
    parameter int DATA_WIDTH  /* verilator public_flat_rd */ = 8
) (
    input  logic [        DATA_WIDTH-1:0] i_data,
    input  logic [$clog2(DATA_WIDTH)-1:0] i_amt,
    output logic [        DATA_WIDTH-1:0] o_data
);

  always_comb begin : rotate
    o_data = '0;
    for (int i = 0; i < DATA_WIDTH; ++i) begin
      int rotate_amt = (int'(i_amt) + i) % DATA_WIDTH;
      o_data[$bits(i_amt)'(rotate_amt)] = i_data[i];
    end
  end : rotate

endmodule : rotate

`endif  /* LIBSV_BIT_OPS_ROTATE */
