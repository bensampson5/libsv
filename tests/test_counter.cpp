#include "Vcounter.h"
#include "verilated.h"
#include "verilated_vpi.h"
#include "catch2/catch.hpp"
#include "test.hpp"

SCENARIO("Counter can be reset") 
{
    GIVEN("A counter") 
    {
        Vcounter* counter = new Vcounter;

        WHEN("reset is asserted")
        {
            counter->aresetn = 0;
            counter->eval();

            THEN("q is set to 0")
            {
                REQUIRE(counter->q == 0);
            }
        }

        delete counter;
    }
}

SCENARIO("Counter can increment and wraparound")
{
    GIVEN("A counter")
    {
        Vcounter* counter = new Vcounter;

        // Get parameter N (number of bits in counter)
        const int N = get_module_parameter("TOP.counter.N");
        REQUIRE(N > 0);
        REQUIRE(N <= 64);
        const uint64_t COUNTER_MAX_VALUE = UINT64_MAX >> (64 - N);

        // Assert reset and set clk low
        counter->aresetn = 0;
        counter->clk = 0;
        counter->eval();

        // De-assert reset
        counter->aresetn = 1;
        counter->eval();

        REQUIRE(counter->q == 0);

        uint64_t prev_q = static_cast<uint64_t>(counter->q);
        WHEN("Clocked")
        {
            THEN("q increments by 1 on every rising edge of clock and wraps around if at max value")
            {
                for (uint64_t i = 0; i < COUNTER_MAX_VALUE; ++i)
                {
                    counter->clk = 1;
                    counter->eval();

                    REQUIRE(static_cast<uint64_t>(counter->q) == prev_q + 1);
                    prev_q = static_cast<uint64_t>(counter->q);

                    counter->clk = 0;
                    counter->eval();
                }

                counter->clk = 1;
                counter->eval();

                REQUIRE(counter->q == 0);

                counter->clk = 0;
                counter->eval();
            }
        }
        
        delete counter;
    }
}