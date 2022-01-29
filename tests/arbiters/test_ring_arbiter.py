import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from utils import pytest_cocotb_run_test


def test_ring_arbiter(pytestconfig):
    """Pytest fixture for Ring Arbiter test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


@cocotb.test()
async def cocotb_test_ring_arbiter(dut):
    """Ring Arbiter test"""

    # ports = int(dut.PORTS)
    # data_width = int(dut.DATA_WIDTH)

    cocotb.fork(Clock(dut.i_clock, 2).start())

    # reset
    dut.i_aresetn.value = 0
    await FallingEdge(dut.i_clock)
    dut.i_aresetn.value = 1

    dut.i_data.value = 0x04030201
    dut.i_input_valid.value = 0b1111

    dut.i_output_ready.value = 1
    for i in range(10):
        await FallingEdge(dut.i_clock)
