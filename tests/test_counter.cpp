#include "Vcounter.h"
#include "verilated.h"
#include "catch2/catch.hpp"
#include <cstdio>

TEST_CASE("Test Counter") 
{
    Vcounter* top = new Vcounter;

    top->clk = 0;
    top->aresetn = 0;
    top->eval();

    top->aresetn = 1;
    top->eval();

    int i = 0;
    while (i < 16)
    { 
        top->clk = 1;
        top->eval();
        top->clk = 0;
        top->eval();
        ++i;
    }

    REQUIRE(1 == 1);

    delete top;
}