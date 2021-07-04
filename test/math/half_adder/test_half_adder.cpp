#include "HalfAdderWrapper.hpp"
#include "catch2/catch.hpp"
#include <string>

const std::string S1 = "Half adder can add";
SCENARIO("" + S1)
{
    GIVEN("A half adder")
    {
        HalfAdderWrapper* haw = new HalfAdderWrapper(S1);

        WHEN("Half adder is provided inputs")
        {
            THEN("It calculates sum and carry values correctly")
            {
                // i_a = 0, i_b = 0
                haw->m_half_adder->i_a = 0;
                haw->m_half_adder->i_b = 0;
                haw->tick();
                REQUIRE(haw->m_half_adder->o_sum == 0);
                REQUIRE(haw->m_half_adder->o_carry == 0);

                // i_a = 0, i_b = 1
                haw->m_half_adder->i_a = 0;
                haw->m_half_adder->i_b = 1;
                haw->tick();
                REQUIRE(haw->m_half_adder->o_sum == 1);
                REQUIRE(haw->m_half_adder->o_carry == 0);

                // i_a = 1, i_b = 0
                haw->m_half_adder->i_a = 1;
                haw->m_half_adder->i_b = 0;
                haw->tick();
                REQUIRE(haw->m_half_adder->o_sum == 1);
                REQUIRE(haw->m_half_adder->o_carry == 0);

                // i_a = 1, i_b = 1
                haw->m_half_adder->i_a = 1;
                haw->m_half_adder->i_b = 1;
                haw->tick();
                REQUIRE(haw->m_half_adder->o_sum == 0);
                REQUIRE(haw->m_half_adder->o_carry == 1);

                haw->tick();
            }
        }
    }
}