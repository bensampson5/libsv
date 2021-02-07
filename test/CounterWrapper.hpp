#ifndef COUNTER_WRAPPER_HPP
#define COUNTER_WRAPPER_HPP

#include <cstdint>
#include <string>
#include "Vcounter.h"
#include "verilated_vcd_c.h"

class CounterWrapper {
private:
    uint64_t m_simTime;

public:
    std::string m_scenarioName;
    Vcounter* m_counter;
    VerilatedVcdC* m_trace;
    uint32_t m_N;

    CounterWrapper(const std::string scenarioName);
    ~CounterWrapper();
    void reset();
    void tick(bool clock = true, uint64_t tickCount = 1);
};

#endif // COUNTER_WRAPPER_HPP