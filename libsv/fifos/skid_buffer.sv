`ifndef LIBSV_FIFOS_SKID_BUFFER
`define LIBSV_FIFOS_SKID_BUFFER

module skid_buffer #(
    parameter int DATA_WIDTH  /* verilator public_flat_rd */ = 32
) (
    input  logic                  i_clock,
    input  logic                  i_aresetn,
    input  logic                  i_clear,
    input  logic [DATA_WIDTH-1:0] i_data,
    input  logic                  i_input_valid,
    input  logic                  i_output_ready,
    output logic [DATA_WIDTH-1:0] o_data,
    output logic                  o_output_valid,
    output logic                  o_input_ready
);

  // CONTROL PATH -----------------------------

  typedef enum logic [2:0] {
    EMPTY = 3'b001,
    BUSY  = 3'b010,
    FULL  = 3'b100
  } state_t;

  state_t state, next_state;  // state variables
  logic accept, transmit;  // handshake flags on each interface
  logic [DATA_WIDTH-1:0] buffer;  // the "skid" buffer

  always_comb begin : next_state_logic
    accept     = i_input_valid && o_input_ready;  // check for input handshake
    transmit   = o_output_valid && i_output_ready;  // check for output handshake
    next_state = EMPTY;
    unique case (state)
      EMPTY: begin
        next_state = EMPTY;
        if (accept) next_state = BUSY;
      end
      BUSY: begin
        next_state = BUSY;
        if (accept && !transmit) next_state = FULL;
        else if (!accept && transmit) next_state = EMPTY;
      end
      FULL: begin
        next_state = FULL;
        if (transmit) next_state = BUSY;
      end
      default: next_state = EMPTY;
    endcase
  end : next_state_logic

  always_ff @(posedge i_clock, negedge i_aresetn) begin : update_state_logic
    if (!i_aresetn || i_clear) begin
      state          <= EMPTY;
      o_input_ready  <= 1'b0;
      o_output_valid <= 1'b0;
    end else begin
      state          <= next_state;
      o_input_ready  <= next_state != FULL;
      o_output_valid <= next_state != EMPTY;
    end
  end : update_state_logic

  logic buffer_write_en, o_data_write_en;
  always_comb begin : write_en_logic
    buffer_write_en = state == BUSY && accept && !transmit;
    o_data_write_en = (state == EMPTY && accept && !transmit)
                      || (state == BUSY && accept && transmit)
                      || (state == FULL && !accept && transmit);
  end : write_en_logic

  // END OF CONTROL PATH ----------------------

  // DATA PATH --------------------------------

  always_ff @(posedge i_clock, negedge i_aresetn) begin : o_data_and_buffer_logic
    if (!i_aresetn || i_clear) begin
      o_data <= '0;
      buffer <= '0;
    end else begin

      if (o_data_write_en) begin
        if (state == FULL) o_data <= buffer;
        else o_data <= i_data;
      end

      if (buffer_write_en) begin
        buffer <= i_data;
      end

    end
  end : o_data_and_buffer_logic

  // END OF DATA PATH -------------------------

endmodule

`endif  /* LIBSV_FIFOS_SKID_BUFFER */
