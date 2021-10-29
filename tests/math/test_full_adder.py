import cocotb
from cocotb.triggers import Timer
from utils import pytest_cocotb_run_test


def test_full_adder(pytestconfig):
    """Pytest fixture for Full Adder test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


@cocotb.test()
async def cocotb_test_full_adder(dut):
    """Full adder test"""

    for i in range(2 ** 3):
        i_a = i & 1
        i_b = (i >> 1) & 1
        i_carry = (i >> 2) & 1
        o_sum = i_a ^ i_b ^ i_carry
        o_carry = ((i_a | i_b) & i_carry) | (i_a & i_b)

        dut.i_a.value = i_a
        dut.i_b.value = i_b
        dut.i_carry.value = i_carry
        await Timer(1)
        assert dut.o_sum == o_sum
        assert dut.o_carry == o_carry
