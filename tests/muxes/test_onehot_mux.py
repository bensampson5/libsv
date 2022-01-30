import cocotb
from cocotb.triggers import Timer
from utils import pytest_cocotb_run_test


def test_onehot_mux(pytestconfig):
    """Pytest fixture for One-hot Mux test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


@cocotb.test()
async def cocotb_test_onehot_mux(dut):
    """One-hot mux test"""

    ports = int(dut.PORTS)
    data_width = int(dut.DATA_WIDTH)

    # Generate counting pattern on input vectors
    dut_i_data = 0
    for i in range(ports):
        dut_i_data |= (i % data_width) << (i * data_width)
    dut.i_data.value = dut_i_data

    for i in range(ports):
        dut.i_select.value = 1 << i
        await Timer(1)
        assert i % data_width == int(dut.o_data)
