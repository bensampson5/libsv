module bcd_encoder #(
    parameter integer N  /* verilator public_flat_rd */ = 8
) (
    input  logic [      N-1:0] bin,
    output logic [N+(N-4)/3:0] bcd
);

  integer i, j;

  always_comb begin
    for (i = 0; i <= N + (N - 4) / 3; i = i + 1) bcd[i] = 0;  // initialize with zeros
    bcd[N-1:0] = bin;  // initialize with input vector
    for (i = 0; i <= N - 4; i = i + 1)  // iterate on structure depth
      for (j = 0; j <= i / 3; j = j + 1)  // iterate on structure width
        if (bcd[N-i+4*j-:4] > 4)  // if > 4
          bcd[N-i+4*j-:4] = bcd[N-i+4*j-:4] + 4'd3;  // add 3
  end

endmodule
