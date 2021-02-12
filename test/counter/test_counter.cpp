#include "CounterWrapper.hpp"
#include "catch2/catch.hpp"
#include <string>

const std::string S1 = "Counter can reset";
SCENARIO("" + S1)
{
    GIVEN("A counter with a non-zero count")
    {
        CounterWrapper* cw = new CounterWrapper(S1);

        // Start with clk low and reset de-asserted
        cw->m_counter->clk = 0;
        cw->m_counter->aresetn = 1;
        cw->tick(false, 0); // initialize trace

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

const std::string S2 = "Counter can increment";
SCENARIO("" + S2)
{
    GIVEN("A counter")
    {
        CounterWrapper* cw = new CounterWrapper(S2);

        REQUIRE(cw->m_N > 0);
        REQUIRE(cw->m_N <= 64);
        const uint64_t COUNTER_MAX_VALUE = UINT64_MAX >> (64 - cw->m_N);

        // Start with clk low and reset de-asserted
        cw->m_counter->clk = 0;
        cw->m_counter->aresetn = 1;
        cw->tick(false, 0); // initialize trace

        // Reset counter so that 'q' is 0
        cw->reset();
        REQUIRE(cw->m_counter->q == 0);

        uint64_t prev_q = static_cast<uint64_t>(cw->m_counter->q);
        WHEN("Clocked")
        {
            THEN("q increments by 1 with every clock cycle and wraps around if at max value")
            {
                // Increment 'q' by clocking the counter until it reaches its max value or does 16 increments, whichever is less
                const uint64_t INCREMENT_COUNT = std::min(static_cast<uint64_t>(16), COUNTER_MAX_VALUE);
                for (uint64_t i = 0; i < INCREMENT_COUNT; ++i) {
                    cw->tick();
                    REQUIRE(cw->m_counter->q == prev_q + 1);
                    prev_q = static_cast<uint64_t>(cw->m_counter->q);
                }
            }
        }

        cw->tick(false); // add one more time step to end of simulation but don't clock
    }
}

const std::string S3 = "Counter can wraparound";
SCENARIO("" + S3)
{
    GIVEN("A counter set to its maximum value")
    {
        CounterWrapper* cw = new CounterWrapper(S3);

        REQUIRE(cw->m_N > 0);
        REQUIRE(cw->m_N <= 64);
        const uint64_t COUNTER_MAX_VALUE = UINT64_MAX >> (64 - cw->m_N);

        // Start with clk low, reset de-asserted, and 'q' at its maximum value
        cw->m_counter->clk = 0;
        cw->m_counter->aresetn = 1;
        cw->m_counter->q = COUNTER_MAX_VALUE;
        cw->tick(false, 0); // initialize trace

        // Increment by 1 so that counter will wraparound to 0
        cw->tick();
        REQUIRE(cw->m_counter->q == 0);
    }
}