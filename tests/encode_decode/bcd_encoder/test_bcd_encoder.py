import cocotb
from cocotb.triggers import Timer
from openhdl_test_utils import pytest_cocotb_run_test


def test_bcd_encoder(pytestconfig):
    """Pytest fixture for BCD Encoder test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


@cocotb.test()
async def cocotb_test_bcd_encoder(dut):
    """BCD Encoder test"""

    # dw = int(dut.DW)
    # n = int(dut.N)

    for i in range(16):
        dut.bin <= i
        await Timer(1)

    # # Generate counting pattern on input vectors
    # dut_i = 0
    # for i in range(n):
    #     dut_i |= (i % dw) << (i * dw)
    # dut.i <= dut_i

    # for i in range(n):
    #     dut.sel <= 1 << i
    #     await Timer(1)
    #     assert i % dw == int(dut.o)
