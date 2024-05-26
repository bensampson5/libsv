import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from cocotb.log import SimLog
from utils import pytest_cocotb_run_test


def test_ring_arbiter(pytestconfig):
    """Pytest fixture for Ring Arbiter test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


@cocotb.test()
async def cocotb_test_ring_arbiter(dut):
    """Ring Arbiter test"""

    log = SimLog("cocotb.test_ring_arbiter")

    ports = int(dut.PORTS)
    data_width = int(dut.DATA_WIDTH)

    cocotb.start_soon(Clock(dut.i_clock, 2).start())

    # reset
    dut.i_aresetn.value = 0
    await FallingEdge(dut.i_clock)
    dut.i_aresetn.value = 1

    # setup i_data
    i_data_array = [i & (2**data_width - 1) for i in range(ports)]
    i_data = 0
    for i in range(ports):
        i_data |= i << (data_width * i)
    log.info("i_data = 0x" + format(i_data, f"0{ports*data_width//4}x"))
    log.info(f"i_data_array = {i_data_array}")
    dut.i_data.value = i_data
    dut.i_input_valid.value = 2**ports - 1

    # Scenario 1: Have all ports have data ready for the arbiter and
    # have output interface be ready to receive data from arbiter. This
    # will test the ring arbiter at max throughput
    dut.i_clear.value = 1
    await FallingEdge(dut.i_clock)
    dut.i_clear.value = 0
    dut.i_output_ready.value = 1
    for i in range(4 * ports):
        await FallingEdge(dut.i_clock)
        if i > 0:
            assert int(dut.o_data.value) == i_data_array[(i % len(i_data_array)) - 1]

    # Scenario 2: Have a port drop out but still maintain max throughput
    # of output interface
    dut.i_input_valid.value = 2**ports - 2  # port 0 drops out
    i_data_array_s2 = i_data_array[1:]
    for i in range(4 * (ports - 1)):
        await FallingEdge(dut.i_clock)
        assert int(dut.o_data.value) == i_data_array_s2[(i % len(i_data_array_s2)) - 1]

    # Scenario 3: Have the output interface backpressure the ring arbiter
    # which should cause it to fill up and backpressure the input interface
    dut.i_output_ready.value = 0
    prev_i_data = int(dut.sb.i_data.value)
    prev_o_data = int(dut.o_data.value)
    await FallingEdge(dut.i_clock)
    # check that output is being held even though input is still accepted
    current_i_data = int(dut.sb.i_data.value)
    assert current_i_data == i_data_array_s2[0] and current_i_data != prev_i_data
    assert int(dut.o_data.value) == prev_o_data
    prev_i_data = int(dut.sb.i_data.value)  # update prev_i_data
    await FallingEdge(dut.i_clock)
    # check that now both input and output are being held
    assert int(dut.sb.i_data.value) == prev_i_data
    assert int(dut.o_data.value) == prev_o_data

    # Scenario 4: Have all ports drop out but release the backpressing of the
    # ring arbiter by the output interface and validate the ring arbiter empties
    dut.i_input_valid.value = 0  # all ports drop out
    dut.i_output_ready.value = 1  # re-enable output interface
    await FallingEdge(dut.i_clock)  # ring arbiter empties skid buffer
    current_o_data = int(dut.o_data.value)
    assert current_o_data != prev_o_data and current_o_data == i_data_array_s2[-1]
    prev_o_data = current_o_data
    await FallingEdge(dut.i_clock)  # ring arbiter empties last entry
    assert dut.o_output_valid.value == 0
