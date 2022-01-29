`ifndef LIBSV_CODERS_ONEHOT_PRIORITY_ENCODER
`define LIBSV_CODERS_ONEHOT_PRIORITY_ENCODER

module onehot_priority_encoder #(
    parameter integer WIDTH  /* verilator public_flat_rd */ = 4
) (
    input  logic [WIDTH-1:0] i_in,
    output logic [WIDTH-1:0] o_out
);

  always_comb begin
    bit stop;
    o_out   = '0;
    stop    = 1'b0;

    for (int i = 0; i < WIDTH; ++i) begin
      if (i_in[i] == 1'b1 && !stop) begin
        o_out[i] = 1'b1;
        stop     = 1'b1;
      end
    end
  end

endmodule : onehot_priority_encoder

`endif  /* LIBSV_CODERS_ONEHOT_PRIORITY_ENCODER */
