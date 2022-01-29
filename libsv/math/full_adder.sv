`ifndef LIBSV_MATH_FULL_ADDER
`define LIBSV_MATH_FULL_ADDER

module full_adder (
    input  logic i_a,
    input  logic i_b,
    input  logic i_carry,
    output logic o_sum,
    output logic o_carry
);

  assign o_sum   = i_a ^ i_b ^ i_carry;
  assign o_carry = ((i_a | i_b) & i_carry) | (i_a & i_b);

endmodule

`endif  /* LIBSV_MATH_FULL_ADDER */
