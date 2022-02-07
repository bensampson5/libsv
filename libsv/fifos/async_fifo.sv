`ifndef LIBSV_FIFOS_ASYNC_FIFO
`define LIBSV_FIFOS_ASYNC_FIFO

`include "libsv/coders/gray_encoder.sv"
`include "libsv/coders/gray_decoder.sv"
`include "libsv/synchronizers/synchronizer.sv"

module async_fifo #(
    parameter int DATA_WIDTH  /* verilator public_flat_rd */ = 8,
    parameter int FIFO_DEPTH  /* verilator public_flat_rd */ = 4
) (
    input  logic                  i_wr_clock,
    input  logic                  i_rd_clock,
    input  logic                  i_aresetn,
    input  logic                  i_wr_en,
    input  logic                  i_rd_en,
    input  logic [DATA_WIDTH-1:0] i_data,
    output logic [DATA_WIDTH-1:0] o_data,
    output logic                  o_full,
    output logic                  o_empty
);

    // WRITE CLOCK DOMAIN -----------------------------------------------------

    typedef enum logic {
        NOT_FULL,
        FULL
    } state_wr_t;
    state_wr_t state_wr, next_state_wr;
    logic [$clog2(FIFO_DEPTH)-1:0]
        wr_addr, wr_addr_gray, next_wr_addr, rd_addr_sync, rd_addr_sync_gray;

    assign o_full       = state_wr == FULL;
    assign next_wr_addr = wr_addr == $bits(wr_addr)'(FIFO_DEPTH - 1) ? '0 : wr_addr + 1'b1;

    always_comb begin : next_state_wr_logic
        unique case (state_wr)
            NOT_FULL: begin
                next_state_wr = NOT_FULL;
                if (i_wr_en && next_wr_addr == rd_addr_sync) next_state_wr = FULL;
            end
            FULL: begin
                next_state_wr = FULL;
                if (wr_addr != rd_addr_sync) next_state_wr = NOT_FULL;
            end
            default: next_state_wr = NOT_FULL;
        endcase
    end : next_state_wr_logic

    always_ff @(posedge i_wr_clock, negedge i_aresetn) begin : state_wr_logic
        if (!i_aresetn) begin
            state_wr <= NOT_FULL;
        end else begin
            state_wr <= next_state_wr;
        end
    end : state_wr_logic

    always_ff @(posedge i_wr_clock, negedge i_aresetn) begin : wr_addr_logic
        if (!i_aresetn) begin
            wr_addr <= '0;
        end else begin
            if (i_wr_en && state_wr != FULL) wr_addr <= next_wr_addr;
        end
    end : wr_addr_logic

    gray_encoder #(
        .DATA_WIDTH($bits(wr_addr))
    ) ge_wr (
        .i_bin (wr_addr),
        .o_gray(wr_addr_gray)
    );

    gray_decoder #(
        .DATA_WIDTH($bits(rd_addr_sync))
    ) gd_wr (
        .i_gray(rd_addr_sync_gray),
        .o_bin (rd_addr_sync)
    );

    generate
        for (genvar i = 0; i < $bits(rd_addr_gray); ++i) begin : gen_rd_addr_sync_gray
            synchronizer #(2) rd_addr_to_wr_domain (
                .i_clock  (i_rd_clock),
                .i_aresetn(i_aresetn),
                .i_data   (rd_addr_gray[i]),
                .o_data   (rd_addr_sync_gray[i])
            );
        end : gen_rd_addr_sync_gray
    endgenerate

    // END OF WRITE CLOCK DOMAIN ----------------------------------------------

    // READ CLOCK DOMAIN ------------------------------------------------------

    typedef enum logic {
        NOT_EMPTY,
        EMPTY
    } state_rd_t;
    state_rd_t state_rd, next_state_rd;
    logic [$clog2(FIFO_DEPTH)-1:0]
        rd_addr, rd_addr_gray, next_rd_addr, wr_addr_sync, wr_addr_sync_gray;

    assign o_empty      = state_rd == EMPTY;
    assign next_rd_addr = rd_addr == $bits(rd_addr)'(FIFO_DEPTH - 1) ? '0 : rd_addr + 1'b1;

    always_comb begin : next_state_rd_logic
        unique case (state_rd)
            NOT_EMPTY: begin
                next_state_rd = NOT_EMPTY;
                if (i_rd_en && next_rd_addr == wr_addr_sync) next_state_rd = EMPTY;
            end
            EMPTY: begin
                next_state_rd = EMPTY;
                if (rd_addr != wr_addr_sync) next_state_rd = NOT_EMPTY;
            end
            default: next_state_rd = EMPTY;
        endcase
    end : next_state_rd_logic

    always_ff @(posedge i_rd_clock, negedge i_aresetn) begin : state_rd_logic
        if (!i_aresetn) begin
            state_rd <= EMPTY;
        end else begin
            state_rd <= next_state_rd;
        end
    end : state_rd_logic

    always_ff @(posedge i_rd_clock, negedge i_aresetn) begin : rd_addr_logic
        if (!i_aresetn) begin
            rd_addr <= '0;
        end else begin
            if (i_rd_en && state_rd == NOT_EMPTY) rd_addr <= next_rd_addr;
        end
    end : rd_addr_logic

    gray_encoder #(
        .DATA_WIDTH($bits(rd_addr))
    ) ge_rd (
        .i_bin (rd_addr),
        .o_gray(rd_addr_gray)
    );

    gray_decoder #(
        .DATA_WIDTH($bits(wr_addr_sync))
    ) gd_rd (
        .i_gray(wr_addr_sync_gray),
        .o_bin (wr_addr_sync)
    );

    generate
        for (genvar i = 0; i < $bits(wr_addr_gray); ++i) begin : gen_wr_addr_sync_gray
            synchronizer #(2) wr_addr_to_rd_domain (
                .i_clock  (i_rd_clock),
                .i_aresetn(i_aresetn),
                .i_data   (wr_addr_gray[i]),
                .o_data   (wr_addr_sync_gray[i])
            );
        end : gen_wr_addr_sync_gray
    endgenerate

    // END OF READ CLOCK DOMAIN -----------------------------------------------

    // FIFO MEMORY
    logic [FIFO_DEPTH-1:0][DATA_WIDTH-1:0] fifo_mem;

    always_ff @(posedge i_wr_clock, negedge i_aresetn) begin : fifo_mem_logic
        if (!i_aresetn) begin
            fifo_mem <= '0;
        end else begin
            if (i_wr_en && state_wr != FULL) fifo_mem[wr_addr] <= i_data;
        end
    end : fifo_mem_logic

    assign o_data = fifo_mem[rd_addr];

endmodule

`endif  /* LIBSV_FIFOS_ASYNC_FIFO */
