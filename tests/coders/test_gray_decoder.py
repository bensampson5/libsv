import cocotb
from cocotb.triggers import Timer
from cocotb.log import SimLog
from utils import pytest_cocotb_run_test


def test_gray_decoder(pytestconfig):
    """Pytest fixture for Gray Decoder test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


@cocotb.test()
async def cocotb_test_gray_decoder(dut):
    """Gray Decoder test"""

    log = SimLog("cocotb.test_gray_decoder")

    data_width = int(dut.DATA_WIDTH)

    for i in range(2**data_width):

        dut.i_gray.value = i
        await Timer(1)

        try:
            assert int(dut.o_bin.value) == gray_decode(i, data_width)
        except AssertionError as e:
            log.info(
                f"i_gray = {dut.i_gray.value}, o_bin = {dut.o_bin.value}, "
                + "gray_decode = "
                + format(gray_decode(i, data_width), f"0{data_width}b")
            )
            raise e


def gray_decode(gray: int, data_width: int) -> int:

    binary = gray & (1 << (data_width - 1))
    for i in range(data_width - 1):
        temp = gray & (1 << i)
        for j in range(i + 1, data_width):
            temp ^= gray >> (j - i)
        binary |= temp & (1 << i)

    return binary
