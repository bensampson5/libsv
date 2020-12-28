#include "Vcounter.h"
#include "verilated.h"
#include <cstdio>

int main(int argc, char** argv, char** env) {
    Verilated::commandArgs(argc, argv);
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

    delete top;
    exit(0);
}