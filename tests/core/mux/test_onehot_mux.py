from cocotb_test.simulator import run
import os
from pathlib import Path
import cocotb
from cocotb.triggers import Timer


def test_onehot_mux(pytestconfig):
    """One-hot mux test."""

    os.environ["SIM"] = "verilator"
    proj_path = Path(pytestconfig.rootpath)
    build_dir = proj_path / "build" / "core" / "mux"

    run(
        verilog_sources=[proj_path / "src" / "core" / "mux" / "onehot_mux.sv"],
        toplevel="onehot_mux",
        module="test_onehot_mux",
        sim_build=build_dir,
        waves=True,
    )

    wavefile = build_dir / "dump.fst"
    if wavefile.exists():
        wavefile.rename(build_dir / "test_onehot_mux.fst")


@cocotb.test()
async def cocotb_test_onehot_mux(dut):
    """One-hot mux test."""

    dw = int(dut.DW)
    n = int(dut.N)

    # Generate counting pattern on input vectors
    dut_i = 0
    for i in range(n):
        dut_i |= (i % dw) << (i * dw)
    dut.i <= dut_i

    for i in range(n):
        dut.sel <= 1 << i
        await Timer(1)
        assert i % dw == int(dut.o)
