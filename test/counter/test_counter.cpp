#include "Vcounter.h"
#include "catch2/catch.hpp"
#include "test.hpp"
#include "verilated.h"
#include <string>

const std::string S1 = "Counter can be reset";
SCENARIO("" + S1)
{
    GIVEN("A counter with a non-zero count")
    {
        ModuleWrapper<Vcounter>* counter = new ModuleWrapper<Vcounter>;
        counter->openTrace(scenario_name_to_vcd_file_name(S1).c_str());

        WHEN("Counter is reset")
        {
            counter->reset();

            THEN("q is set to 0")
            {
                REQUIRE(counter->m_core->q == 0);

                REQUIRE(1 == 0);
            }
        }
    }
}

const std::string S2 = "Counter can increment and wraparound";
SCENARIO("" + S2)
{
    GIVEN("A counter")
    {
        ModuleWrapper<Vcounter>* top = new ModuleWrapper<Vcounter>;
        top->openTrace(scenario_name_to_vcd_file_name(S2).c_str());

        // Get parameter N (number of bits in counter)
        const int N = get_module_parameter("TOP.counter.N");
        REQUIRE(N > 0);
        REQUIRE(N <= 64);
        const uint64_t COUNTER_MAX_VALUE = UINT64_MAX >> (64 - N);

        // Reset counter so that 'q' is 0
        top->reset();
        REQUIRE(top->m_core->q == 0);

        uint64_t prev_q = static_cast<uint64_t>(top->m_core->q);
        WHEN("Clocked")
        {
            THEN("q increments by 1 with every clock cycle and wraps around if at max value")
            {
                // Increment 'q' by clocking the counter until it reaches its max value
                for (uint64_t i = 0; i < COUNTER_MAX_VALUE; ++i) {
                    top->tick();
                    REQUIRE(top->m_core->q == prev_q + 1);
                    prev_q = static_cast<uint64_t>(top->m_core->q);
                }

                // Increment q one more time and check that it wrapped around to 0
                top->tick();
                REQUIRE(top->m_core->q == 0);
            }
        }
    }
}