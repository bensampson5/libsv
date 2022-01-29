`ifndef LIBSV_ARBITERS_RING_ARBITER
`define LIBSV_ARBITERS_RING_ARBITER

`include "libsv/bit_ops/rotate.sv"
`include "libsv/coders/onehot_priority_encoder.sv"

module ring_arbiter #(
    parameter int PORTS /* verilator public_flat_rd */ = 4,
    parameter int WIDTH /* verilator public_flat_rd */ = 8
) (
    input logic i_clock,
    input logic i_aresetn,

    // This is a bummer. Would much rather do:
    //     input logic [PORTS-1:0][WIDTH-1:0] i_data
    // and have a 2D packed array but verilator doesn't
    // support 2D packed arrays using VPI which is what 
    // cocotb uses. See https://github.com/verilator/verilator/issues/2812.
    input logic [PORTS*WIDTH-1:0] i_data,
    
    input logic [PORTS-1:0] i_valid,
    output logic [WIDTH-1:0] o_data,
    output logic [PORTS-1:0] o_ready
);

    // START OF CONTROL PATH LOGIC --------------------------

    // pre-rotate
    logic [$clog2(PORTS)-1:0] pre_rotate_amt;
    wire [PORTS-1:0] pre_rotate_out;
    rotate #(PORTS) pre_rotate (
        .i_in(i_valid),
        .i_amt(pre_rotate_amt),
        .o_out(pre_rotate_out)
    );

    // select highest priority queue
    wire [PORTS-1:0] ohpe_out;
    wire ohpe_valid;
    onehot_priority_encoder #(PORTS) ohpe (
        .i_in(pre_rotate_out),
        .o_out(ohpe_out),
        .o_valid(ohpe_valid)
    );

    // post-rotate (undo the pre-rotate)
    logic [$clog2(PORTS)-1:0] post_rotate_amt;
    wire [PORTS-1:0] post_rotate_out;
    rotate #(PORTS) post_rotate (
        .i_in(ohpe_out),
        .i_amt(post_rotate_amt),
        .o_out(post_rotate_out)
    );

    // drive o_ready to select next queue to empty
    assign o_ready = post_rotate_out;

    // capture current state of o_ready
    logic [PORTS-1:0] prev_o_ready;
    always_ff @(posedge i_clock, negedge i_aresetn) begin
        if (i_aresetn == 0) begin
            prev_o_ready <= '0;
        end else begin
            prev_o_ready <= o_ready;
        end
    end

    // rotate controller logic
    always_comb begin : rotate_controller
        pre_rotate_amt = '0;
        post_rotate_amt = '0;
        for (int i = 0; i < $bits(prev_o_ready); ++i) begin
            if (prev_o_ready[i]) begin
                pre_rotate_amt = 2'(PORTS - i - 1);
                post_rotate_amt = 2'(i + 1);
            end
        end
    end : rotate_controller

    // END OF CONTROL PATH LOGIC ----------------------------

    // Dummy implementation
    assign o_data = '0;

endmodule : ring_arbiter

`endif /* LIBSV_ARBITERS_RING_ARBITER */