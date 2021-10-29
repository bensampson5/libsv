import cocotb
from cocotb.triggers import Timer
from utils import pytest_cocotb_run_test


def test_sr_latch(pytestconfig):
    """Pytest fixture for SR Latch test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


@cocotb.test()
async def cocotb_test_sr_latch(dut):
    """SR Latch test"""

    dut.s.value = 0
    dut.r.value = 0
    await Timer(1)

    dut.s.value = 1
    await Timer(1)
    assert dut.q == 1
    assert dut.q_n == 0

    dut.s.value = 0
    await Timer(1)

    dut.r.value = 1
    await Timer(1)
    assert dut.q == 0
    assert dut.q_n == 1
