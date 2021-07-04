#ifndef COUNTER_WRAPPER_HPP
#define COUNTER_WRAPPER_HPP

#include "Vcounter.h"
#include "verilated_vcd_c.h"
#include <cstdint>
#include <string>

class CounterWrapper {
private:
    uint64_t m_simTime;
    VerilatedVcdC* m_trace;

public:
    std::string m_scenarioName;
    Vcounter* m_counter;
    uint32_t m_N;

    CounterWrapper(std::string scenarioName);
    ~CounterWrapper();
    void reset();
    void tick(bool clock = true, uint64_t tickCount = 1);
};

#endif // COUNTER_WRAPPER_HPP