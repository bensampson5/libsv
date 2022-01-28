module onehot_priority_encoder #(
    parameter integer IW  /* verilator public_flat_rd */ = 4
) (
    input  logic [IW-1:0] i_in,
    output logic [IW-1:0] o_out,
    output logic          o_valid
);

  always_comb begin
    bit stop;
    o_out   = '0;
    o_valid = 1'b0;
    stop    = 1'b0;

    for (int i = 0; i < IW; ++i) begin
      if (i_in[i] == 1'b1 && !stop) begin
        o_out[i] = 1'b1;
        o_valid  = 1'b1;
        stop     = 1'b1;
      end
    end
  end

endmodule
