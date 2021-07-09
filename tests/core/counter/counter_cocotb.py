import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge


@cocotb.test()
async def test_counter(dut):
    """Counter test."""

    n = int(dut.N)

    cocotb.fork(Clock(dut.clk, 2).start())

    # reset
    dut.aresetn <= 0
    await FallingEdge(dut.clk)
    dut.aresetn <= 1

    # increment through all possible counter states
    for i in range(2 ** n):
        await RisingEdge(dut.clk)
        assert int(dut.q) == i

    # increment once more and check roll-over condition
    await RisingEdge(dut.clk)
    assert int(dut.q) == 0
