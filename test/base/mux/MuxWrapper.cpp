#include "MuxWrapper.hpp"
#include "Vmux.h"
#include "test.hpp"
#include "verilated.h"
#include "verilated_vcd_c.h"
#include <cstdint>
#include <string>

MuxWrapper::MuxWrapper(std::string scenarioName)
{
    m_scenarioName = scenarioName;
    m_mux = new Vmux;
    m_simTime = 0;

    // setup trace
    Verilated::traceEverOn(true);
    m_trace = new VerilatedVcdC;
    m_mux->trace(m_trace, 99);
    m_trace->open(scenarioNameToVcdFilename(m_scenarioName).c_str());

    // Save parameter 'N' to class member variable
    m_N = getModuleParameter("TOP.mux.N");
    m_DW = getModuleParameter("TOP.mux.DW");
}

MuxWrapper::~MuxWrapper()
{
    m_trace->close();
    m_trace = nullptr;
    delete m_mux;
    m_mux = nullptr;
}
