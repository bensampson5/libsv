import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from utils import pytest_cocotb_run_test


def test_synchonrizer(pytestconfig):
    """Pytest fixture for Synchronizer test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


@cocotb.test()
async def cocotb_test_synchonrizer(dut):
    """Synchronizer test"""

    ff_stages = int(dut.FF_STAGES)

    cocotb.fork(Clock(dut.i_clock, 2).start())

    dut.i_aresetn.value = 0
    await FallingEdge(dut.i_clock)
    dut.i_aresetn.value = 1

    sync_value = 1
    dut.i_data.value = sync_value
    for _ in range(ff_stages):
        assert dut.o_data.value != sync_value
        await FallingEdge(dut.i_clock)

    assert dut.o_data.value == sync_value
