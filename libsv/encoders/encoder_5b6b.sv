module encoder_5b6b (
    input  logic [4:0] i_5b,
    input  logic       i_rd,
    input  logic       i_is_control,
    output logic [5:0] o_6b,
    output logic       o_rd
);

  always_comb begin
    case (i_5b)
      // Mapping is EDCBA : iedcba
      5'b00000: begin  // D.00
        o_6b = i_rd ? 6'b000110 : 6'b111001;
        o_rd = ~i_rd;
      end
      5'b00001: begin  // D.01
        o_6b = i_rd ? 6'b010001 : 6'b101110;
        o_rd = ~i_rd;
      end
      5'b00010: begin  // D.02
        o_6b = i_rd ? 6'b010010 : 6'b101101;
        o_rd = ~i_rd;
      end
      5'b00011: begin  // D.03
        o_6b = 6'b100011;
        o_rd = i_rd;
      end
      5'b00100: begin  // D.04
        o_6b = i_rd ? 6'b010100 : 6'b101011;
        o_rd = ~i_rd;
      end
      5'b00101: begin  // D.05
        o_6b = 6'b100101;
        o_rd = i_rd;
      end
      5'b00110: begin  // D.06
        o_6b = 6'b100110;
        o_rd = i_rd;
      end
      5'b00111: begin  // D.07
        o_6b = i_rd ? 6'b111000 : 6'b000111;
        o_rd = ~i_rd;
      end
      5'b01000: begin  // D.08
        o_6b = i_rd ? 6'b011000 : 6'b100111;
        o_rd = ~i_rd;
      end
      5'b01001: begin  // D.09
        o_6b = 6'b101001;
        o_rd = i_rd;
      end
      5'b01010: begin  // D.10
        o_6b = 6'b101010;
        o_rd = i_rd;
      end
      5'b01011: begin  // D.11
        o_6b = 6'b001011;
        o_rd = i_rd;
      end
      5'b01100: begin  // D.12
        o_6b = 6'b101100;
        o_rd = i_rd;
      end
      5'b01101: begin  // D.13
        o_6b = 6'b001101;
        o_rd = i_rd;
      end
      5'b01110: begin  // D.14
        o_6b = 6'b001110;
        o_rd = i_rd;
      end
      5'b01111: begin  // D.15
        o_6b = i_rd ? 6'b000101 : 6'b111010;
        o_rd = ~i_rd;
      end
      5'b10000: begin  // D.16
        o_6b = i_rd ? 6'b001001 : 6'b110110;
        o_rd = ~i_rd;
      end
      5'b10001: begin  // D.17
        o_6b = 6'b110001;
        o_rd = i_rd;
      end
      5'b10010: begin  // D.18
        o_6b = 6'b110010;
        o_rd = i_rd;
      end
      5'b10011: begin  // D.19
        o_6b = 6'b010011;
        o_rd = i_rd;
      end
      5'b10100: begin  // D.20
        o_6b = 6'b110100;
        o_rd = i_rd;
      end
      5'b10101: begin  // D.21
        o_6b = 6'b010101;
        o_rd = i_rd;
      end
      5'b10110: begin  // D.22
        o_6b = 6'b010110;
        o_rd = i_rd;
      end
      5'b10111: begin  // D.23
        o_6b = i_rd ? 6'b101000 : 6'b010111;
        o_rd = ~i_rd;
      end
      5'b11000: begin  // D.24
        o_6b = i_rd ? 6'b001100 : 6'b110011;
        o_rd = ~i_rd;
      end
      5'b11001: begin  // D.25
        o_6b = 6'b011001;
        o_rd = i_rd;
      end
      5'b11010: begin  // D.26
        o_6b = 6'b011010;
        o_rd = i_rd;
      end
      5'b11011: begin  // D.27
        o_6b = i_rd ? 6'b100100 : 6'b011011;
        o_rd = ~i_rd;
      end
      5'b11100: begin
        if (i_is_control) begin  // K.28
          o_6b = i_rd ? 6'b000011 : 6'b111100;
          o_rd = ~i_rd;
        end else begin  // D.28
          o_6b = 6'b011100;
          o_rd = i_rd;
        end
      end
      5'b11101: begin  // D.29
        o_6b = i_rd ? 6'b100010 : 6'b011101;
        o_rd = ~i_rd;
      end
      5'b11110: begin  // D.30
        o_6b = i_rd ? 6'b100001 : 6'b011110;
        o_rd = ~i_rd;
      end
      5'b11111: begin  // D.31
        o_6b = i_rd ? 6'b001010 : 6'b110101;
        o_rd = ~i_rd;
      end
      default: begin  // default case is D.0
        o_6b = i_rd ? 6'b000110 : 6'b111001;
        o_rd = ~i_rd;
      end
    endcase
  end

endmodule
