import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from utils import pytest_cocotb_run_test


def test_skid_buffer(pytestconfig):
    """Pytest fixture for Skid Buffer test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


@cocotb.test()
async def cocotb_test_skid_buffer(dut):
    """Skid Buffer test"""

    data_width = int(dut.DATA_WIDTH)

    cocotb.start_soon(Clock(dut.i_clock, 2).start())

    # reset
    dut.i_aresetn.value = 0
    await FallingEdge(dut.i_clock)
    dut.i_aresetn.value = 1

    # generate data and have both input and output interfaces
    # be ready.
    i_data = 0
    o_data = 0
    dut.i_data.value = i_data
    dut.i_input_valid.value = 1
    dut.i_output_ready.value = 1

    # stream at full rate for 4 transactions
    for _ in range(4):
        await FallingEdge(dut.i_clock)
        o_data = i_data
        assert int(dut.o_data.value) == o_data  # check output data
        i_data = (i_data + 1) % (2**data_width)
        dut.i_data.value = i_data  # drive next input data

    # disable output ready so that skid buffer gets full
    dut.i_output_ready.value = 0
    await FallingEdge(dut.i_clock)
    for _ in range(4):
        await FallingEdge(dut.i_clock)
        assert int(dut.o_data.value) == o_data

    # re-enable output ready but disable input valid so that
    # buffer empties
    dut.i_output_ready.value = 1
    dut.i_input_valid.value = 0
    for _ in range(4):
        await FallingEdge(dut.i_clock)
        if o_data < i_data:
            o_data += 1
        assert int(dut.o_data.value) == o_data  # check output data

    # continue streaming for another few transactions
    dut.i_input_valid.value = 1
    dut.i_output_ready.value = 1
    for _ in range(4):
        await FallingEdge(dut.i_clock)
        o_data = i_data
        assert int(dut.o_data.value) == o_data  # check output data
        i_data = (i_data + 1) % (2**data_width)
        dut.i_data.value = i_data  # drive next input data

    await FallingEdge(dut.i_clock)
