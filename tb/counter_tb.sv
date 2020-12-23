// Author: Ben Sampson
`include "../src/counter.v"
`timescale 1ns/1ns

`define CLK_HALF_PERIOD 1

module counter_tb;

    localparam N = 4;
    
    reg clk;
    reg aresetn;
    wire[N-1:0] q;

    counter #(.N(N)) counter_0(.clk(clk), .aresetn(aresetn), .q(q));

    always #`CLK_HALF_PERIOD clk = ~clk;

    initial begin
        $dumpfile("counter_tb.vcd");
        $dumpvars(0, counter_tb);

        $monitor("Time = %0t clk = %0d q = %0d", $time, clk, q);

        clk <= 1;
        aresetn <= 0;
        #1 aresetn <= 1;

        #50 $finish;
    end

endmodule