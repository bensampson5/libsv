#ifndef TEST_HPP
#define TEST_HPP

#include "verilated.h"
#include "verilated_vcd_c.h"
#include <cstdint>

// Verilator VPI needs these
extern vluint64_t main_time;
double sc_time_stamp();

int get_module_parameter(const char* const handle);
std::string scenario_name_to_vcd_file_name(const std::string scenario_name);

template <class Module>
class ModuleWrapper {
    uint64_t m_simTime;

public:
    Module* m_core;
    VerilatedVcdC* m_trace;

    ModuleWrapper(void)
    {
        m_core = new Module;

        // Start with clk low and reset de-asserted
        m_core->clk = 0;
        m_core->aresetn = 1;

        Verilated::traceEverOn(true);
        m_simTime = 0;
        m_trace = nullptr;
    }

    virtual ~ModuleWrapper(void)
    {
        this->closeTrace();
        delete m_core;
        m_core = nullptr;
    }

    virtual void openTrace(const char* const vcdName)
    {
        if (!m_trace) {
            m_trace = new VerilatedVcdC;
            m_core->trace(m_trace, 99);
            m_trace->open(vcdName);
            this->tick(false, 0); // initialize trace
        }
    }

    virtual void closeTrace(void)
    {
        if (m_trace) {
            m_trace->close();
            m_trace = nullptr;
        }
    }

    virtual void reset(void)
    {
        m_core->aresetn = 0;
        this->tick(false);
        m_core->aresetn = 1;
        this->tick(false);
    }

    virtual void tick(bool clock = true, uint64_t tick_count = 1)
    {
        if (clock) {
            for (uint64_t i = 0; i < tick_count; ++i) {
                m_core->clk = 1;
                m_core->eval();
                if (m_trace)
                    m_trace->dump(++m_simTime);

                m_core->clk = 0;
                m_core->eval();
                if (m_trace)
                    m_trace->dump(++m_simTime);
            }
        } else {
            m_simTime += tick_count;
            m_core->eval();
            if (m_trace)
                m_trace->dump(m_simTime);
        }

        m_trace->flush();
    }
};

#endif // TEST_HPP