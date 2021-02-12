#include "CounterWrapper.hpp"
#include "Vcounter.h"
#include "test.hpp"
#include "verilated.h"
#include "verilated_vcd_c.h"
#include <string>

CounterWrapper::CounterWrapper(const std::string scenarioName)
{
    m_scenarioName = scenarioName;
    m_counter = new Vcounter;
    m_simTime = 0;

    Verilated::traceEverOn(true);
    m_trace = new VerilatedVcdC;
    m_counter->trace(m_trace, 99);
    m_trace->open(scenarioNameToVcdFilename(m_scenarioName).c_str());

    // Save parameter 'N' to class member variable
    m_N = getModuleParameter("TOP.counter.N");

    // Start with clk low and reset de-asserted
    m_counter->clk = 0;
    m_counter->aresetn = 1;
    this->tick(false, 0); // initialize trace
}

CounterWrapper::~CounterWrapper()
{
    m_trace->close();
    m_trace = nullptr;
    delete m_counter;
    m_counter = nullptr;
}

void CounterWrapper::reset()
{
    m_counter->aresetn = 0;
    this->tick(false);
    m_counter->aresetn = 1;
    this->tick(false);
}

void CounterWrapper::tick(bool clock, uint64_t tickCount)
{
    if (clock) {
        for (uint64_t i = 0; i < tickCount; ++i) {
            m_counter->clk = 1;
            m_counter->eval();
            if (m_trace)
                m_trace->dump(++m_simTime);

            m_counter->clk = 0;
            m_counter->eval();
            if (m_trace)
                m_trace->dump(++m_simTime);
        }
    } else {
        m_simTime += tickCount;
        m_counter->eval();
        if (m_trace)
            m_trace->dump(m_simTime);
    }

    m_trace->flush();
}