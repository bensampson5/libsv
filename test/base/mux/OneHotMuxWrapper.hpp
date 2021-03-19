#ifndef ONEHOT_MUX_WRAPPER_HPP
#define ONEHOT_MUX_WRAPPER_HPP

#include "Vonehot_mux.h"
#include "verilated_vcd_c.h"
#include <cstdint>
#include <string>

class OneHotMuxWrapper {
private:
    uint64_t m_simTime;
    VerilatedVcdC* m_trace;

public:
    std::string m_scenarioName;
    Vonehot_mux* m_onehot_mux;
    uint32_t m_N;
    uint64_t m_DW;

    OneHotMuxWrapper(std::string scenarioName);
    ~OneHotMuxWrapper();

    void tick(uint64_t tickCount = 1);
};

#endif // MUX_WRAPPER_HPP