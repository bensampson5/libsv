import cocotb
from cocotb.triggers import Timer
from utils import pytest_cocotb_run_test


def test_priority_encoder(pytestconfig):
    """Pytest fixture for Priority Encoder test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


@cocotb.test()
async def cocotb_test_priority_encoder(dut):
    """Priority Encoder test"""

    data_width = int(dut.DATA_WIDTH)

    for i in range(2**data_width):
        dut.i_data.value = i  # drive input

        await Timer(1)

        # check valid signal
        if i == 0:
            assert dut.o_valid == 0
        else:
            result = priority_encode(i, data_width)
            assert dut.o_valid == 1
            assert dut.o_data == result  # check output


def priority_encode(x: int, data_width: int) -> int:

    test = 0
    for shift_amt in range(data_width):

        test = x & (1 << shift_amt)

        if test > 0:
            return shift_amt

    return 0
