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

    cocotb.fork(Clock(dut.i_clock, 2).start())

    # reset
    dut.i_aresetn.value = 0
    await FallingEdge(dut.i_clock)
    dut.i_aresetn.value = 1

    # setup i_data
    i_data_array = [ports - i - 1 for i in range(ports)]
    i_data = 0
    for i in range(ports):
        i_data |= (ports - i - 1) << (data_width * (ports - i - 1))
    log.info("i_data = 0x" + format(i_data, f"0{ports*data_width//4}x"))
    log.info(f"i_data_array = {i_data_array}")
    dut.i_data.value = i_data
    dut.i_input_valid.value = 2 ** ports - 1

    # Scenario 1: Have all ports have data ready for the arbiter and
    # have output interface be ready to receive data from arbiter. This
    # will test the ring arbiter at max throughput
    dut.i_output_ready.value = 1
    for i in range(4 * ports):
        await FallingEdge(dut.i_clock)
        if i > 0:
            assert (int(dut.o_data.value) + 1) % ports == i % ports

    # Scenario 2: Have a port drop out but still maintain max throughput
    # of output interface
    # TODO

    # Scenario 3: Have the output interface backpressure the ring arbiter
    # which should cause it to fill up and backpressure the input interface
    # TODO

    # Scenario 4: Have all ports drop out but release the backpressing of the
    # ring arbiter by the output interface and watch the ring arbiter go empty
    # TODO
