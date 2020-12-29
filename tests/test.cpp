#define CATCH_CONFIG_MAIN
#include "catch2/catch.hpp"
#include "verilated.h"
#include "verilated_vpi.h"

// For verilator's VPI
vluint64_t main_time = 0;
double sc_time_stamp() { return main_time; }

int get_module_parameter(const char* const handle)
{
    vpiHandle vh = vpi_handle_by_name((PLI_BYTE8*)handle, NULL);
    s_vpi_value v;
    v.format = vpiIntVal;
    vpi_get_value(vh, &v);
    return v.value.integer;
}