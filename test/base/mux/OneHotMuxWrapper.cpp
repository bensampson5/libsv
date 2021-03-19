#include "OneHotMuxWrapper.hpp"
#include "Vonehot_mux.h"
#include "test.hpp"
#include "verilated.h"
#include "verilated_vcd_c.h"
#include <cstdint>
#include <string>

OneHotMuxWrapper::OneHotMuxWrapper(std::string scenarioName)
{
    m_scenarioName = scenarioName;
    m_onehot_mux = new Vonehot_mux;
    m_simTime = 0;

    // setup trace
    Verilated::traceEverOn(true);
    m_trace = new VerilatedVcdC;
    m_onehot_mux->trace(m_trace, 99);
    m_trace->open(scenarioNameToVcdFilename(m_scenarioName).c_str());

    // Save parameter 'N' to class member variable
    m_N = getModuleParameter("TOP.onehot_mux.N");
    m_DW = getModuleParameter("TOP.onehot_mux.DW");
}

OneHotMuxWrapper::~OneHotMuxWrapper()
{
    m_trace->close();
    m_trace = nullptr;
    delete m_onehot_mux;
    m_onehot_mux = nullptr;
}

void OneHotMuxWrapper::tick(uint64_t tickCount)
{
    m_simTime += tickCount;
    m_onehot_mux->eval();
    if (m_trace)
        m_trace->dump(m_simTime);

    m_trace->flush();
}
