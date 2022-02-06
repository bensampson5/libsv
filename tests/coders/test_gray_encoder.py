import cocotb
from cocotb.triggers import Timer
from cocotb.log import SimLog
from utils import pytest_cocotb_run_test


def test_gray_encoder(pytestconfig):
    """Pytest fixture for Gray Encoder test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


@cocotb.test()
async def cocotb_test_gray_encoder(dut):
    """Gray Encoder test"""

    log = SimLog("cocotb.test_gray_encoder")

    data_width = int(dut.DATA_WIDTH)

    for i in range(2 ** data_width):
        dut.i_bin.value = i
        await Timer(1)

        try:
            assert int(dut.o_gray.value) == gray_encode(i, data_width)
        except AssertionError as e:
            log.info(
                f"i_bin = {dut.i_bin.value}, o_gray = {dut.o_gray.value}, "
                + "gray_encode = "
                + format(gray_encode(i, data_width), f"0{data_width}b")
            )
            raise e


def gray_encode(binary: int, data_width: int) -> int:

    gray = binary & (1 << (data_width - 1))
    for i in range(data_width - 1):
        gray |= (binary ^ (binary >> 1)) & (1 << i)

    return gray
