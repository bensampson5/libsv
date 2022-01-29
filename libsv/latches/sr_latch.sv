`ifndef LIBSV_LATCHES_SR_LATCH
`define LIBSV_LATCHES_SR_LATCH

module sr_latch (
    input  logic                                 s,
    input  logic                                 r,
    output logic  /* verilator lint_off UNOPT */ q  /* verilator lint_on UNOPT */,
    output logic                                 q_n
);

  assign q   = ~(r | q_n);
  assign q_n = ~(s | q);

endmodule

`endif  /* LIBSV_LATCHES_SR_LATCH */
