module bcd_encoder (
    input  logic [3:0] bin,
    output logic [7:0] bcd
);

  always_comb begin
    case (bin)
      4'h0:    bcd = 8'h00;
      4'h1:    bcd = 8'h01;
      4'h2:    bcd = 8'h02;
      4'h3:    bcd = 8'h03;
      4'h4:    bcd = 8'h04;
      4'h5:    bcd = 8'h05;
      4'h6:    bcd = 8'h06;
      4'h7:    bcd = 8'h07;
      4'h8:    bcd = 8'h08;
      4'h9:    bcd = 8'h09;
      4'hA:    bcd = 8'h10;
      4'hB:    bcd = 8'h11;
      4'hC:    bcd = 8'h12;
      4'hD:    bcd = 8'h13;
      4'hE:    bcd = 8'h14;
      4'hF:    bcd = 8'h15;
      default: bcd = 8'h00;
    endcase
  end


endmodule
