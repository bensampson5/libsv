import cocotb
from cocotb.triggers import Timer
from utils import pytest_cocotb_run_test


def test_bcd_decoder(pytestconfig):
    """Pytest fixture for BCD Decoder test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


@cocotb.test()
async def cocotb_test_bcd_decoder(dut):
    """BCD Decoder test"""

    n = int(dut.N)

    for i in range(10**n):
        dut.i_bcd.value = int(str(int(i)), 16)
        await Timer(1)
        assert dut.o_bin == i
