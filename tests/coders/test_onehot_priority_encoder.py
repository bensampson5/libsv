import cocotb
from cocotb.triggers import Timer
from utils import pytest_cocotb_run_test


def test_onehot_priority_encoder(pytestconfig):
    """Pytest fixture for Priority Encoder test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


@cocotb.test()
async def cocotb_test_onehot_priority_encoder(dut):
    """One-hot Priority Encoder test"""

    width = int(dut.WIDTH)

    for i in range(2 ** width):
        dut.i_in.value = i  # drive input

        await Timer(1)

        result = onehot_priority_encode(i, width)
        assert dut.o_out == result  # check output


def onehot_priority_encode(x: int, width: int) -> int:

    test = 0
    for shift_amt in range(width):

        test = x & (1 << shift_amt)

        if test > 0:
            return test

    return 0
