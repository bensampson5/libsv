`ifndef LIBSV_CODERS_ONEHOT_PRIORITY_ENCODER
`define LIBSV_CODERS_ONEHOT_PRIORITY_ENCODER

module onehot_priority_encoder #(
    parameter int DATA_WIDTH  /* verilator public_flat_rd */ = 4
) (
    input  logic [DATA_WIDTH-1:0] i_data,
    output logic [DATA_WIDTH-1:0] o_data
);

    always_comb begin
        bit stop;
        o_data = '0;
        stop   = 1'b0;

        for (int i = 0; i < DATA_WIDTH; ++i) begin
            if (i_data[i] == 1'b1 && !stop) begin
                o_data[i] = 1'b1;
                stop      = 1'b1;
            end
        end
    end

endmodule : onehot_priority_encoder

`endif  /* LIBSV_CODERS_ONEHOT_PRIORITY_ENCODER */
