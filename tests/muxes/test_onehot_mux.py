import cocotb
from cocotb.triggers import Timer
from utils import pytest_cocotb_run_test


def test_onehot_mux(pytestconfig):
    """Pytest fixture for One-hot Mux test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


@cocotb.test()
async def cocotb_test_onehot_mux(dut):
    """One-hot mux test"""

    dw = int(dut.DW)
    n = int(dut.N)

    # Generate counting pattern on input vectors
    dut_i = 0
    for i in range(n):
        dut_i |= (i % dw) << (i * dw)
    dut.i.value = dut_i

    for i in range(n):
        dut.sel.value = 1 << i
        await Timer(1)
        assert i % dw == int(dut.o)
