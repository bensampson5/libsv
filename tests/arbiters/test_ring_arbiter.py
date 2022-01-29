import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge
from cocotb.log import SimLog
from utils import pytest_cocotb_run_test


def test_ring_arbiter(pytestconfig):
    """Pytest fixture for Ring Arbiter test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


@cocotb.test()
async def cocotb_test_ring_arbiter(dut):
    """Ring Arbiter test"""

    log = SimLog("cocotb.test_ring_arbiter")

    ports = int(dut.PORTS)
    width = int(dut.WIDTH)

    cocotb.fork(Clock(dut.i_clock, 2).start())

    # reset
    dut.i_aresetn.value = 0
    await FallingEdge(dut.i_clock)
    dut.i_aresetn.value = 1
    await FallingEdge(dut.i_clock)

    dut.i_data.value = 0x04030201
    dut.i_valid.value = 0b001

    for i in range(5):
        await FallingEdge(dut.i_clock)

    dut.i_valid.value = 0b101

    for i in range(5):
        await FallingEdge(dut.i_clock)

    dut.i_valid.value = 0b111

    for i in range(5):
        await FallingEdge(dut.i_clock)
