#ifndef MUX_WRAPPER_HPP
#define MUX_WRAPPER_HPP

#include "Vmux.h"
#include "verilated_vcd_c.h"
#include <cstdint>
#include <string>

class MuxWrapper {
private:
    uint64_t m_simTime;
    VerilatedVcdC* m_trace;

public:
    std::string m_scenarioName;
    Vmux* m_mux;
    uint32_t m_N;
    uint64_t m_DW;

    MuxWrapper(std::string scenarioName);
    ~MuxWrapper();
};

#endif // MUX_WRAPPER_HPP