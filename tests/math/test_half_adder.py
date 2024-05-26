import cocotb
from cocotb.triggers import Timer
from utils import pytest_cocotb_run_test


def test_half_adder(pytestconfig):
    """Pytest fixture for Half Adder test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


@cocotb.test()
async def cocotb_test_half_adder(dut):
    """Half adder test"""

    for i in range(2**2):
        i_a = i & 1
        i_b = (i >> 1) & 1
        o_sum = i_a ^ i_b
        o_carry = i_a & i_b

        dut.i_a.value = i_a
        dut.i_b.value = i_b
        await Timer(1)
        assert dut.o_sum == o_sum
        assert dut.o_carry == o_carry
