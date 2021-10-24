import cocotb
from cocotb.triggers import Timer
from libsv_test_utils import pytest_cocotb_run_test


def test_bcd_encoder(pytestconfig):
    """Pytest fixture for BCD Encoder test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


@cocotb.test()
async def cocotb_test_bcd_encoder(dut):
    """BCD Encoder test"""

    n = int(dut.N)

    for i in range(2 ** n):
        dut.i_bin <= i
        await Timer(1)
        assert dut.o_bcd == int(str(int(dut.i_bin)), 16)
