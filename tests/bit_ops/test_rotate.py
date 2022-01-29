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

    width = int(dut.WIDTH.value)
    amt_bits = len(dut.i_amt.value)

    for value in range(2 ** width):

        for amt in range(2 ** amt_bits):

            dut.i_in.value = value
            dut.i_amt.value = amt
            await Timer(1)

            o_out_expected = 0
            try:
                o_out_expected = do_rotate(value, amt, width)
                assert o_out_expected == dut.o_out.value
                log.debug(
                    f"PASSED: i_in = 0b{dut.i_in.value}, i_amt = 0b{dut.i_amt.value}, "
                    f"o_out = 0b{dut.o_out.value}, o_out_expected = 0b"
                    + format(o_out_expected, f"0{width}b")
                )
            except AssertionError as e:
                log.critical(
                    f"FAILED: i_in = 0b{dut.i_in.value}, i_amt = 0b{dut.i_amt.value}, "
                    f"o_out = 0b{dut.o_out.value}, o_out_expected = 0b"
                    + format(o_out_expected, f"0{width}b")
                )
                raise e


def do_rotate(value: int, amt: int, width: int):
    width_mask = 2 ** width - 1
    adj_amt = amt % width  # adjust amount if greater than width
    return ((value << adj_amt) & width_mask) | (
        (value >> (width - adj_amt)) & width_mask
    )
