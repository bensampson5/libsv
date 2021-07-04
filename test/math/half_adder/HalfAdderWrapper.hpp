#ifndef HALF_ADDER_WRAPPER_HPP
#define HALF_ADDER_WRAPPER_HPP

#include "Vhalf_adder.h"
#include "verilated_vcd_c.h"
#include <cstdint>
#include <string>

class HalfAdderWrapper {
private:
    uint64_t m_simTime;
    VerilatedVcdC* m_trace;

public:
    std::string m_scenarioName;
    Vhalf_adder* m_half_adder;

    HalfAdderWrapper(std::string scenarioName);
    ~HalfAdderWrapper();

    void tick(uint64_t tickCount = 1);
};

#endif // HALF_ADDER_WRAPPER_HPP