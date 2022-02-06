`ifndef LIBSV_CODERS_GRAY_ENCODER
`define LIBSV_CODERS_GRAY_ENCODER

module gray_encoder #(
    parameter int DATA_WIDTH  /* verilator public_flat_rd */ = 8
) (
    input  logic [DATA_WIDTH-1:0] i_bin,
    output logic [DATA_WIDTH-1:0] o_gray
);

    always_comb begin
        o_gray = '0;
        for (int i = 0; i < DATA_WIDTH - 1; ++i) begin
            o_gray[i] = i_bin[i] ^ i_bin[i+1];
        end
        o_gray[DATA_WIDTH-1] = i_bin[DATA_WIDTH-1];
    end

endmodule

`endif  /* LIBSV_CODERS_GRAY_ENCODER */
