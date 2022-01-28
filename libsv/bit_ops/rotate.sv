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
      o_out[i_amt+i[$bits(i_amt)-1:0]] = i_in[i];
    end
  end : rotate

endmodule
