`ifndef LIBSV_CODERS_BCD_DECODER
`define LIBSV_CODERS_BCD_DECODER

module bcd_decoder #(
    parameter integer N  /* verilator public_flat_rd */ = 3
) (
    input  logic [        4*N-1:0] i_bcd,
    output logic [3*N+(N+2)/3-1:0] o_bin
);

    integer i, j;

    logic [4*N-1:0] temp;  // create temp vector as wide as i_bcd to hold intermediate values
    always_comb begin
        temp = i_bcd;  // initialize with input vector
        for (i = 0; i < 4 * (N - 1); i = i + 1)  // iterate on structure depth
            for (j = 0; j < N - i / 4 - 1; j = j + 1)  // iterate on structure width
                if (temp[4+i+4*j-:4] > 7)  // if > 7
                    temp[4+i+4*j-:4] = temp[4+i+4*j-:4] - 4'd3;  // subtract three
        o_bin = temp[3*N+(N+2)/3-1:0];  // truncate final result in temp vector to get o_bin
    end

endmodule

`endif  /* LIBSV_CODERS_BCD_DECODER */
