import cocotb
from cocotb.triggers import Timer
from cocotb.log import SimLog
from utils import pytest_cocotb_run_test


def test_rotate(pytestconfig):
    """Pytest fixture for Rotate test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


@cocotb.test()
async def cocotb_test_rotate(dut):
    """Rotate test"""

    log = SimLog("cocotb.test_rotate")

    data_width = int(dut.DATA_WIDTH.value)
    amt_bits = len(dut.i_amt.value)

    for value in range(2 ** data_width):

        for amt in range(2 ** amt_bits):

            dut.i_data.value = value
            dut.i_amt.value = amt
            await Timer(1)

            o_data_expected = 0
            try:
                o_data_expected = do_rotate(value, amt, data_width)
                assert o_data_expected == dut.o_data.value
                log.debug(
                    f"PASSED: i_data = 0b{dut.i_data.value}, i_amt = "
                    f"0b{dut.i_amt.value}, o_data = 0b{dut.o_data.value}, "
                    "o_data_expected = 0b" + format(o_data_expected, f"0{data_width}b")
                )
            except AssertionError as e:
                log.critical(
                    f"FAILED: i_data = 0b{dut.i_data.value}, i_amt = "
                    f"0b{dut.i_amt.value}, o_data = 0b{dut.o_data.value}, "
                    "o_data_expected = 0b" + format(o_data_expected, f"0{data_width}b")
                )
                raise e


def do_rotate(value: int, amt: int, data_width: int):
    data_width_mask = 2 ** data_width - 1
    adj_amt = amt % data_width  # adjust amount if greater than data_width
    return ((value << adj_amt) & data_width_mask) | (
        (value >> (data_width - adj_amt)) & data_width_mask
    )
