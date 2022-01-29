`ifndef LIBSV_FIFOS_SKID_BUFFER
`define LIBSV_FIFOS_SKID_BUFFER

module skid_buffer #(
    parameter int DATA_WIDTH  /* verilator public_flat_rd */ = 32
) (
    input  logic                  i_clock,
    input  logic                  i_aresetn,
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
  state_t state, next_state;

  // Next state logic
  logic accept, transmit;  // handshake flags on each interface
  always_comb begin : next_state_logic
    accept     = i_input_valid && o_input_ready;  // successful upstream handshake
    transmit   = o_output_valid && i_output_ready;  // successful downstream handshake
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

  // Update state
  always_ff @(posedge i_clock, negedge i_aresetn) begin : update_state
    if (!i_aresetn) state <= EMPTY;
    else state <= next_state;
  end : update_state

  // set o_input_ready (ready for input interface)
  // As long as we're not FULL, data can be accepted
  always_ff @(posedge i_clock, negedge i_aresetn) begin : o_input_ready_logic
    if (!i_aresetn) o_input_ready <= 1'b0;
    else o_input_ready <= next_state != FULL;
  end : o_input_ready_logic

  // set o_output_valid (valid for output interface)
  // As long as we're not EMPTY, data can be transmitted
  always_ff @(posedge i_clock, negedge i_aresetn) begin : o_output_valid_logic
    if (!i_aresetn) o_output_valid <= 1'b0;
    else o_output_valid <= next_state != EMPTY;
  end : o_output_valid_logic

  // Datapath control signals
  logic buffer_write_en, o_data_write_en;

  always_comb begin : buffer_write_en_logic
    buffer_write_en = state == BUSY && accept && !transmit;
  end : buffer_write_en_logic

  always_comb begin : o_data_write_en_logic
    o_data_write_en = (state == EMPTY && accept && !transmit)
                      || (state == BUSY && accept && transmit)
                      || (state == FULL && !accept && transmit);
  end : o_data_write_en_logic

  // END OF CONTROL PATH ----------------------

  // DATA PATH --------------------------------

  // The skid buffer, buffer, is only used when the current
  // state is BUSY but another transaction is being accepted.
  // The buffer and o_data are controlled using write enables
  // and the current state.
  logic [DATA_WIDTH-1:0] buffer;

  // o_data logic
  always_ff @(posedge i_clock, negedge i_aresetn) begin
    if (!i_aresetn) o_data <= '0;
    else if (o_data_write_en) begin
      if (state == FULL) o_data <= buffer;
      else o_data <= i_data;
    end
  end

  // buffer reg logic
  always_ff @(posedge i_clock, negedge i_aresetn) begin
    if (!i_aresetn) buffer <= '0;
    else if (buffer_write_en) buffer <= i_data;
  end

  // END OF DATA PATH -------------------------

endmodule

`endif  /* LIBSV_FIFOS_SKID_BUFFER */
