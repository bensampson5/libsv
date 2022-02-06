`ifndef LIBSV_CODERS_GRAY_DECODER
`define LIBSV_CODERS_GRAY_DECODER

module gray_decoder #(
    parameter int DATA_WIDTH  /* verilator public_flat_rd */ = 8
) (
    input  logic [DATA_WIDTH-1:0] i_gray,
    output logic [DATA_WIDTH-1:0] o_bin
);

    always_comb begin
        o_bin = '0;
        for (int i = 0; i < DATA_WIDTH - 1; ++i) begin
            for (int j = i; j < DATA_WIDTH; ++j) begin
                o_bin[i] ^= i_gray[j];
            end
        end
        o_bin[DATA_WIDTH-1] = i_gray[DATA_WIDTH-1];
    end

endmodule

`endif  /* LIBSV_CODERS_GRAY_DECODER */
