`ifndef LIBSV_FIFOS_SYNC_FIFO
`define LIBSV_FIFOS_SYNC_FIFO

module sync_fifo #(
    parameter int DATA_WIDTH  /* verilator public_flat_rd */ = 8,
    parameter int FIFO_DEPTH  /* verilator public_flat_rd */ = 4
) (
    input  logic                  i_clock,
    input  logic                  i_aresetn,
    input  logic                  i_wr_en,
    input  logic                  i_rd_en,
    input  logic [DATA_WIDTH-1:0] i_data,
    output logic [DATA_WIDTH-1:0] o_data,
    output logic                  o_full,
    output logic                  o_empty
);

    typedef enum logic [2:0] {
        EMPTY = 3'b001,
        BUSY  = 3'b010,
        FULL  = 3'b100
    } state_t;

    state_t state, next_state;
    logic write, read;  // variables that hold if write or read is happening
    logic [$clog2(FIFO_DEPTH)-1:0] wr_addr, rd_addr;
    logic [$clog2(FIFO_DEPTH)-1:0] next_wr_addr, next_rd_addr;
    logic [FIFO_DEPTH-1:0][DATA_WIDTH-1:0] fifo_mem;

    // Logic for status outputs empty and full
    always_ff @(posedge i_clock, negedge i_aresetn) begin
        if (!i_aresetn) begin
            o_empty <= 1'b1;
            o_full  <= 1'b0;
        end else begin
            o_empty <= next_state == EMPTY;
            o_full  <= next_state == FULL;
        end
    end

    always_comb begin : next_state_logic
        write = i_wr_en && (state != FULL);
        read  = i_rd_en && (state != EMPTY);

        unique case (state)
            EMPTY: begin
                next_state = EMPTY;
                if (write) next_state = BUSY;
            end
            BUSY: begin
                next_state = BUSY;
                if (read && !write && next_rd_addr == wr_addr) next_state = EMPTY;
                else if (!read && write && next_wr_addr == rd_addr) next_state = FULL;
            end
            FULL: begin
                next_state = FULL;
                if (read) next_state = BUSY;
            end
            default: next_state = EMPTY;
        endcase
    end : next_state_logic

    always_ff @(posedge i_clock, negedge i_aresetn) begin : current_state_logic
        if (!i_aresetn) begin
            state <= EMPTY;
        end else begin
            state <= next_state;
        end
    end : current_state_logic

    always_comb begin : next_wr_rd_addr_logic
        next_wr_addr = wr_addr == $bits(wr_addr)'(FIFO_DEPTH - 1) ? '0 : wr_addr + 1'b1;
        next_rd_addr = rd_addr == $bits(rd_addr)'(FIFO_DEPTH - 1) ? '0 : rd_addr + 1'b1;
    end : next_wr_rd_addr_logic

    always_ff @(posedge i_clock, negedge i_aresetn) begin : update_rd_wr_addr
        if (!i_aresetn) begin
            rd_addr <= '0;
            wr_addr <= '0;
        end else begin
            wr_addr <= write ? next_wr_addr : wr_addr;
            rd_addr <= read ? next_rd_addr : rd_addr;
        end
    end : update_rd_wr_addr

    always_ff @(posedge i_clock, negedge i_aresetn) begin : data_path_logic
        if (!i_aresetn) begin
            fifo_mem <= '0;
        end else begin
            if (write) fifo_mem[wr_addr] <= i_data;
        end
    end : data_path_logic

    assign o_data = fifo_mem[rd_addr];

endmodule

`endif  /* LIBSV_FIFOS_SYNC_FIFO */
