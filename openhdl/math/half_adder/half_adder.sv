module half_adder (
    input  logic i_a,
    input  logic i_b,
    output logic o_sum,
    output logic o_carry
);

  assign o_sum   = i_a ^ i_b;
  assign o_carry = i_a & i_b;

endmodule
