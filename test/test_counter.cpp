#include "CounterWrapper.hpp"
#include "catch2/catch.hpp"
#include <string>

const std::string S1 = "Counter can be reset";
SCENARIO("" + S1)
{
    GIVEN("A counter with a non-zero count")
    {
        CounterWrapper* cw = new CounterWrapper(S1);

        // increment counter so 'q' is non-zero
        cw->tick();
        REQUIRE(cw->m_counter->q != 0);

        WHEN("Counter is reset")
        {
            cw->reset();

            THEN("q is set to 0")
            {
                REQUIRE(cw->m_counter->q == 0);
            }
        }
    }
}

const std::string S2 = "Counter can increment and wraparound";
SCENARIO("" + S2)
{
    GIVEN("A counter")
    {
        CounterWrapper* cw = new CounterWrapper(S2);

        REQUIRE(cw->m_N > 0);
        REQUIRE(cw->m_N <= 64);
        const uint64_t COUNTER_MAX_VALUE = UINT64_MAX >> (64 - cw->m_N);

        // Reset counter so that 'q' is 0
        cw->reset();
        REQUIRE(cw->m_counter->q == 0);

        uint64_t prev_q = static_cast<uint64_t>(cw->m_counter->q);
        WHEN("Clocked")
        {
            THEN("q increments by 1 with every clock cycle and wraps around if at max value")
            {
                // Increment 'q' by clocking the counter until it reaches its max value
                for (uint64_t i = 0; i < COUNTER_MAX_VALUE; ++i) {
                    cw->tick();
                    REQUIRE(cw->m_counter->q == prev_q + 1);
                    prev_q = static_cast<uint64_t>(cw->m_counter->q);
                }

                // Increment q one more time and check that it wrapped around to 0
                cw->tick();
                REQUIRE(cw->m_counter->q == 0);
            }
        }
    }
}