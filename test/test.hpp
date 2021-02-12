#ifndef TEST_HPP
#define TEST_HPP

#include "verilated.h"
#include <cstdint>
#include <string>

// Verilator VPI needs these
extern vluint64_t main_time;
double sc_time_stamp();

int getModuleParameter(const std::string handle);
std::string scenarioNameToVcdFilename(const std::string scenario_name);

#endif // TEST_HPP