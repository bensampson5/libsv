`ifndef LIBSV_ARBITERS_RING_ARBITER
`define LIBSV_ARBITERS_RING_ARBITER

`include "libsv/bit_ops/rotate.sv"
`include "libsv/coders/onehot_priority_encoder.sv"
`include "libsv/muxes/onehot_mux.sv"
`include "libsv/fifos/skid_buffer.sv"

module ring_arbiter #(
    parameter int PORTS  /* verilator public_flat_rd */      = 4,
    parameter int DATA_WIDTH  /* verilator public_flat_rd */ = 8
) (
    input  logic                        i_clock,
    input  logic                        i_aresetn,
    input  logic                        i_clear,
    // This is a bummer. Would much rather do:
    //     input logic [PORTS-1:0][DATA_WIDTH-1:0] i_data
    // and have a 2D packed array but verilator doesn't
    // support 2D packed arrays using VPI which is what
    // cocotb uses. See https://github.com/verilator/verilator/issues/2812.
    input  logic [PORTS*DATA_WIDTH-1:0] i_data,
    input  logic [           PORTS-1:0] i_input_valid,
    input  logic                        i_output_ready,
    output logic [      DATA_WIDTH-1:0] o_data,
    output logic                        o_output_valid,
    output logic [           PORTS-1:0] o_input_ready,
    output logic                        o_accept,
    output logic                        o_transmit
);

    logic [$clog2(PORTS)-1:0] pre_rotate_amt;
    logic [        PORTS-1:0] pre_rotate_out;
    logic [        PORTS-1:0] ohpe_out;
    logic                     ohpe_valid;
    logic [$clog2(PORTS)-1:0] post_rotate_amt;
    logic [        PORTS-1:0] post_rotate_out;
    logic [        PORTS-1:0] prev_accepted;
    logic accept, transmit;
    logic                  is_any_input_valid;
    logic                  input_ready;
    logic [DATA_WIDTH-1:0] ohm_out;

    // CONTROL PATH -------------------------------

    // pre-rotate
    rotate #(PORTS) pre_rotate (
        .i_data(i_input_valid),
        .i_amt (pre_rotate_amt),
        .o_data(pre_rotate_out)
    );

    // onehot priority encoder selects the current highest priority input port
    onehot_priority_encoder #(PORTS) ohpe (
        .i_data(pre_rotate_out),
        .o_data(ohpe_out)
    );

    // post-rotate (undo the pre-rotate)
    rotate #(PORTS) post_rotate (
        .i_data(ohpe_out),
        .i_amt (post_rotate_amt),
        .o_data(post_rotate_out)
    );

    always_ff @(posedge i_clock, negedge i_aresetn) begin : prev_accepted_logic
        if (!i_aresetn || i_clear) begin
            prev_accepted <= '0;
        end else begin
            if (accept) prev_accepted <= post_rotate_out;
            else prev_accepted <= prev_accepted;
        end
    end : prev_accepted_logic

    always_comb begin : rotate_controller
        pre_rotate_amt  = '0;
        post_rotate_amt = '0;
        for (int i = 0; i < $bits(prev_accepted); ++i) begin
            if (prev_accepted[i]) begin
                pre_rotate_amt  = $bits(pre_rotate_amt)'(PORTS - i - 1);
                post_rotate_amt = $bits(post_rotate_amt)'(i + 1);
            end
        end
    end : rotate_controller

    assign is_any_input_valid = |i_input_valid;
    assign o_input_ready      = {PORTS{input_ready}} & post_rotate_out;
    assign o_accept           = accept;
    assign o_transmit         = transmit;

    // END OF CONTROL PATH ------------------------

    // DATA PATH ----------------------------------

    onehot_mux #(
        .PORTS     (PORTS),
        .DATA_WIDTH(DATA_WIDTH)
    ) ohm (
        .i_data  (i_data),
        .i_select(post_rotate_out),
        .o_data  (ohm_out)
    );

    skid_buffer #(DATA_WIDTH) sb (
        .i_clock       (i_clock),
        .i_aresetn     (i_aresetn),
        .i_clear       (i_clear),
        .i_data        (ohm_out),
        .i_input_valid (is_any_input_valid),
        .i_output_ready(i_output_ready),
        .o_data        (o_data),
        .o_output_valid(o_output_valid),
        .o_input_ready (input_ready),
        .o_accept      (accept),
        .o_transmit    (transmit)
    );

    // END OF DATA PATH ---------------------------

endmodule : ring_arbiter

`endif  /* LIBSV_ARBITERS_RING_ARBITER */
