#include "HalfAdderWrapper.hpp"
#include "Vhalf_adder.h"
#include "test.hpp"
#include "verilated.h"
#include "verilated_vcd_c.h"
#include <cstdint>
#include <string>

HalfAdderWrapper::HalfAdderWrapper(std::string scenarioName)
{
    m_scenarioName = scenarioName;
    m_half_adder = new Vhalf_adder;
    m_simTime = 0;

    // setup trace
    Verilated::traceEverOn(true);
    m_trace = new VerilatedVcdC;
    m_half_adder->trace(m_trace, 99);
    m_trace->open(scenarioNameToVcdFilename(m_scenarioName).c_str());
}

HalfAdderWrapper::~HalfAdderWrapper()
{
    m_trace->close();
    m_trace = nullptr;
    delete m_half_adder;
    m_half_adder = nullptr;
}

void HalfAdderWrapper::tick(uint64_t tickCount)
{
    m_simTime += tickCount;
    m_half_adder->eval();
    if (m_trace)
        m_trace->dump(m_simTime);

    m_trace->flush();
}
