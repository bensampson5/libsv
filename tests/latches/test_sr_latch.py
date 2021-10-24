import cocotb
from cocotb.triggers import Timer
from openhdl_test_utils import pytest_cocotb_run_test


def test_sr_latch(pytestconfig):
    """Pytest fixture for SR Latch test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


@cocotb.test()
async def cocotb_test_sr_latch(dut):
    """SR Latch test"""

    dut.s <= 0
    dut.r <= 0
    await Timer(1)

    dut.s <= 1
    await Timer(1)
    assert dut.q == 1
    assert dut.q_n == 0

    dut.s <= 0
    await Timer(1)

    dut.r <= 1
    await Timer(1)
    assert dut.q == 0
    assert dut.q_n == 1
