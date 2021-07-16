from cocotb_test.simulator import run
import os
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge


def test_counter(pytestconfig):
    """Counter test."""

    os.environ["SIM"] = "verilator"
    proj_path = Path(pytestconfig.rootpath)
    build_dir = proj_path / "build" / "core" / "counter"

    run(
        verilog_sources=[proj_path / "src" / "core" / "counter" / "counter.sv"],
        toplevel="counter",
        module="test_counter",
        sim_build=build_dir,
        waves=True,
    )

    wavefile = build_dir / "dump.fst"
    if wavefile.exists():
        wavefile.rename(build_dir / "test_counter.fst")


@cocotb.test()
async def cocotb_test_counter(dut):
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
