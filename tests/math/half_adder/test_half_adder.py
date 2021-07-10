from cocotb_test.simulator import run
import os
from pathlib import Path


def test_half_adder(pytestconfig):

    os.environ["SIM"] = "verilator"
    proj_path = Path(pytestconfig.rootpath)
    build_dir = proj_path / "build" / "math" / "half_adder"

    run(
        verilog_sources=[proj_path / "src" / "math" / "half_adder" / "half_adder.sv"],
        toplevel="half_adder",
        module="half_adder_cocotb",
        sim_build=build_dir,
        waves=True,
    )

    wavefile = build_dir / "dump.fst"
    if wavefile.exists():
        wavefile.rename(build_dir / "test_half_adder.fst")
