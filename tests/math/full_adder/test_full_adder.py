from cocotb_test.simulator import run
import os
from pathlib import Path


def test_full_adder(pytestconfig):
    """Full adder test."""

    os.environ["SIM"] = "verilator"
    proj_path = Path(pytestconfig.rootpath)
    build_dir = proj_path / "build" / "math" / "full_adder"

    run(
        verilog_sources=[proj_path / "src" / "math" / "full_adder" / "full_adder.sv"],
        toplevel="full_adder",
        module="full_adder_cocotb",
        sim_build=build_dir,
        waves=True,
    )

    wavefile = build_dir / "dump.fst"
    if wavefile.exists():
        wavefile.rename(build_dir / "test_full_adder.fst")
