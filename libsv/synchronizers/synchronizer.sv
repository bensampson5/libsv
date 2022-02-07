`ifndef LIBSV_SYNCHRONIZERS_SYNCHRONIZER
`define LIBSV_SYNCHRONIZERS_SYNCHRONIZER

module synchronizer #(
    parameter int DATA_WIDTH  /* verilator public_flat_rd */ = 1,
    parameter int FF_STAGES  /* verilator public_flat_rd */  = 2
) (
    input  logic                  i_clock,
    input  logic                  i_aresetn,
    input  logic [DATA_WIDTH-1:0] i_data,
    output logic [DATA_WIDTH-1:0] o_data
);

    logic [FF_STAGES-1:0][DATA_WIDTH-1:0] sync_mem;

    always_ff @(posedge i_clock, negedge i_aresetn) begin
        if (!i_aresetn) begin
            sync_mem <= '0;
        end else begin
            sync_mem[0] <= i_data;
            for (int i = 1; i < FF_STAGES; ++i) begin
                sync_mem[i] <= sync_mem[i-1];
            end
        end
    end

    assign o_data = sync_mem[FF_STAGES-1];

endmodule

`endif  /* LIBSV_SYNCHRONIZERS_SYNCHRONIZER */
