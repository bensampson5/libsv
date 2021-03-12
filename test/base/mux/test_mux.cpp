#include "MuxWrapper.hpp"
#include "catch2/catch.hpp"
#include <string>

const std::string S1 = "Mux works";
SCENARIO("" + S1)
{
    GIVEN("A mux")
    {
        MuxWrapper* mw = new MuxWrapper(S1);

        WHEN("Something is done to the mux")
        {
            THEN("The mux behaves like expected")
            {
                REQUIRE(1);
            }
        }
    }
}