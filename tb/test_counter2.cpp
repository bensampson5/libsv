#include "Vcounter.h"
#include "verilated.h"
#include "catch_amalgamated.hpp"
#include <cstdio>

TEST_CASE("Test Counter 2") 
{
    Vcounter* top = new Vcounter;

    top->clk = 0;
    top->aresetn = 0;
    top->eval();

    top->aresetn = 1;
    top->eval();

    // printf("N = %i\n", top->N);

    int i = 0;
    while (i < 16)
    { 
        top->clk = 1;
        top->eval();
        top->clk = 0;
        top->eval();

        printf("q = %i\n", top->q);

        ++i;
    }

    REQUIRE(1 == 1);

    delete top;
}