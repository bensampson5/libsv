import cocotb
from cocotb.triggers import Timer
from openhdl_test_utils import pytest_cocotb_run_test


def test_bcd_encoder(pytestconfig):
    """Pytest fixture for BCD Encoder test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


@cocotb.test()
async def cocotb_test_bcd_encoder(dut):
    """BCD Encoder test"""

    n = int(dut.N)

    for i in range(2 ** n):
        dut.bin <= i
        await Timer(1)
        assert dut.bcd == int(str(int(dut.bin)), 16)