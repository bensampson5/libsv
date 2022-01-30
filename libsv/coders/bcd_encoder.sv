`ifndef LIBSV_CODERS_BCD_ENCODER
`define LIBSV_CODERS_BCD_ENCODER

module bcd_encoder #(
    parameter integer N  /* verilator public_flat_rd */ = 8
) (
    input  logic [      N-1:0] i_bin,
    output logic [N+(N-4)/3:0] o_bcd
);

    integer i, j;

    always_comb begin
        o_bcd = {{(N - 4) / 3 + 1{1'b0}}, i_bin};  // initialize with input vector in lower bits
        for (i = 0; i <= N - 4; i = i + 1)  // iterate on structure depth
            for (j = 0; j <= i / 3; j = j + 1)  // iterate on structure width
                if (o_bcd[N-i+4*j-:4] > 4)  // if > 4
                    o_bcd[N-i+4*j-:4] = o_bcd[N-i+4*j-:4] + 4'd3;  // add 3
    end

endmodule

`endif  /* LIBSV_CODERS_BCD_ENCODER */
