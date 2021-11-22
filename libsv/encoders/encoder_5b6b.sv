module encoder_5b6b (
    input logic [4:0] i_5b,
    input logic i_rd,
    input logic i_is_control,
    output logic [5:0] o_6b,
    output logic o_rd
);

    always_comb begin
        case (i_5b)
            // Mapping is EDCBA : iedcba
            5'b00000: begin o_6b = i_rd ? 6'b000110 : 6'b111001; o_rd = ~i_rd; end // D.00
            5'b00001: begin o_6b = i_rd ? 6'b010001 : 6'b101110; o_rd = ~i_rd; end // D.01
            5'b00010: begin o_6b = i_rd ? 6'b010010 : 6'b101101; o_rd = ~i_rd; end // D.02
            5'b00011: begin o_6b = 6'b100011; o_rd = i_rd; end                     // D.03
            5'b00100: begin o_6b = i_rd ? 6'b010100 : 6'b101011; o_rd = ~i_rd; end // D.04
            5'b00101: begin o_6b = 6'b100101; o_rd = i_rd; end                     // D.05
            5'b00110: begin o_6b = 6'b100110; o_rd = i_rd; end                     // D.06
            5'b00111: begin o_6b = i_rd ? 6'b111000 : 6'b000111; o_rd = ~i_rd; end // D.07
            5'b01000: begin o_6b = i_rd ? 6'b011000 : 6'b100111; o_rd = ~i_rd; end // D.08
            5'b01001: begin o_6b = 6'b101001; o_rd = i_rd; end                     // D.09
            5'b01010: begin o_6b = 6'b101010; o_rd = i_rd; end                     // D.10
            5'b01011: begin o_6b = 6'b001011; o_rd = i_rd; end                     // D.11
            5'b01100: begin o_6b = 6'b101100; o_rd = i_rd; end                     // D.12
            5'b01101: begin o_6b = 6'b001101; o_rd = i_rd; end                     // D.13
            5'b01110: begin o_6b = 6'b001110; o_rd = i_rd; end                     // D.14
            5'b01111: begin o_6b = i_rd ? 6'b000101 : 6'b111010; o_rd = ~i_rd; end // D.15
            5'b10000: begin o_6b = i_rd ? 6'b001001 : 6'b110110; o_rd = ~i_rd; end // D.16
            5'b10001: begin o_6b = 6'b110001; o_rd = i_rd; end                     // D.17
            5'b10010: begin o_6b = 6'b110010; o_rd = i_rd; end                     // D.18
            5'b10011: begin o_6b = 6'b010011; o_rd = i_rd; end                     // D.19
            5'b10100: begin o_6b = 6'b110100; o_rd = i_rd; end                     // D.20
            5'b10101: begin o_6b = 6'b010101; o_rd = i_rd; end                     // D.21
            5'b10110: begin o_6b = 6'b010110; o_rd = i_rd; end                     // D.22
            5'b10111: begin o_6b = i_rd ? 6'b101000 : 6'b010111; o_rd = ~i_rd; end // D.23
            5'b11000: begin o_6b = i_rd ? 6'b001100 : 6'b110011; o_rd = ~i_rd; end // D.24
            5'b11001: begin o_6b = 6'b011001; o_rd = i_rd; end                     // D.25
            5'b11010: begin o_6b = 6'b011010; o_rd = i_rd; end                     // D.26
            5'b11011: begin o_6b = i_rd ? 6'b100100 : 6'b011011; o_rd = ~i_rd; end // D.27
            5'b11100: begin
                if (i_is_control) begin
                    o_6b = i_rd ? 6'b000011 : 6'b111100; o_rd = ~i_rd;             // K.28
                end else begin
                    o_6b = 6'b011100; o_rd = i_rd;                                 // D.28
                end
            end                     
            5'b11101: begin o_6b = i_rd ? 6'b100010 : 6'b011101; o_rd = ~i_rd; end // D.29
            5'b11110: begin o_6b = i_rd ? 6'b100001 : 6'b011110; o_rd = ~i_rd; end // D.30
            5'b11111: begin o_6b = i_rd ? 6'b001010 : 6'b110101; o_rd = ~i_rd; end // D.31
        endcase
    end

endmodule;