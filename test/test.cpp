#define CATCH_CONFIG_MAIN
#include "test.hpp"
#include "catch2/catch.hpp"
#include "verilated.h"
#include "verilated_vpi.h"
#include <string>

// Verilator VPI needs these
vluint64_t main_time = 0;
double sc_time_stamp() { return main_time; }

int getModuleParameter(const std::string handle)
{
    vpiHandle vh = vpi_handle_by_name((PLI_BYTE8*)handle.c_str(), NULL);
    s_vpi_value v;
    v.format = vpiIntVal;
    vpi_get_value(vh, &v);
    return v.value.integer;
}

std::string scenarioNameToVcdFilename(const std::string scenario_name)
{
    std::string vcd_name = scenario_name;
    std::for_each(vcd_name.begin(), vcd_name.end(), [](char& c) {
        c = ::tolower(c);
        if (c == ' ')
            c = '_';
    });
    vcd_name += ".vcd";
    return vcd_name;
}