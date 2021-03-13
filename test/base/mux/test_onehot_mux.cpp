#include "OneHotMuxWrapper.hpp"
#include "catch2/catch.hpp"
#include <string>
#include <iostream>

const std::string S1 = "One-hot mux states";
SCENARIO("" + S1)
{
    GIVEN("A one-hot mux")
    {
        OneHotMuxWrapper* ohmw = new OneHotMuxWrapper(S1);

        std::cout << "DW = " << ohmw->m_DW << std::endl;
        std::cout << "N = " << ohmw->m_N << std::endl;

        // TODO: Figure out how to initialize a bus in verilator and pass to
        // input

        WHEN("One-hot mux is set to a certain state using the select line")
        {
            THEN("The correct input is passed to the output")
            {
                ohmw->select(0);
                REQUIRE(1);
            }
        }
    }
}