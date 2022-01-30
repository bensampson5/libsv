`ifndef LIBSV_MUXES_ONEHOT_MUX
`define LIBSV_MUXES_ONEHOT_MUX

module onehot_mux #(
    parameter int PORTS  /* verilator public_flat_rd */      = 4,
    parameter int DATA_WIDTH  /* verilator public_flat_rd */ = 8
) (
    input  logic [PORTS*DATA_WIDTH-1:0] i_data,
    input  logic [           PORTS-1:0] i_select,
    output logic [      DATA_WIDTH-1:0] o_data
);

  always_comb begin
    o_data = '0;
    for (int i = 0; i < PORTS; ++i) begin
      o_data |= {(DATA_WIDTH) {i_select[i]}} & i_data[((i+1)*DATA_WIDTH-1)-:DATA_WIDTH];
    end
  end

endmodule : onehot_mux

`endif  /* LIBSV_MUXES_ONEHOT_MUX */
