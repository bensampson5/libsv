`ifndef LIBSV_CODERS_PRIORITY_ENCODER
`define LIBSV_CODERS_PRIORITY_ENCODER

module priority_encoder #(
    parameter integer DATA_WIDTH  /* verilator public_flat_rd */ = 4
) (
    input  logic [        DATA_WIDTH-1:0] i_data,
    output logic [$clog2(DATA_WIDTH)-1:0] o_data,
    output logic                          o_valid
);

    always_comb begin
        bit stop;
        o_data  = '0;
        o_valid = 1'b0;
        stop    = 1'b0;

        for (int i = 0; i < DATA_WIDTH; ++i) begin
            if (i_data[i] == 1'b1 && !stop) begin
                o_data  = $clog2(DATA_WIDTH)'(i);
                o_valid = 1'b1;
                stop    = 1'b1;
            end
        end
    end

endmodule

`endif  /* LIBSV_CODERS_PRIORITY_ENCODER */
