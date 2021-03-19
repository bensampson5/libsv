#include "OneHotMuxWrapper.hpp"
#include "catch2/catch.hpp"
#include <string>

const std::string S1 = "One-hot mux can mux";
SCENARIO("" + S1)
{
    GIVEN("A one-hot mux")
    {
        OneHotMuxWrapper* ohmw = new OneHotMuxWrapper(S1);

        WHEN("One-hot mux is configured using select")
        {
            THEN("The output is set to the selected input")
            {
                // Reset input and sel to 0
                ohmw->m_onehot_mux->in = 0;
                ohmw->m_onehot_mux->sel = 0;
                ohmw->tick();

                // Generate counting pattern in input vector starting with 0
                ohmw->m_onehot_mux->in = 0;
                for (auto i = 0; i < ohmw->m_N; ++i) {
                    ohmw->m_onehot_mux->in |= (i % ohmw->m_DW) << (i * ohmw->m_DW);
                }

                for (auto i = 0; i < ohmw->m_N; ++i) {
                    ohmw->m_onehot_mux->sel = 1 << i;
                    ohmw->tick();

                    REQUIRE(i % ohmw->m_DW == ohmw->m_onehot_mux->out);
                }
                ohmw->tick();
            }
        }
    }
}