from cocotb_test.simulator import run
import os
from pathlib import Path


def test_counter(pytestconfig):
    """Counter test."""

    os.environ["SIM"] = "verilator"
    proj_path = Path(pytestconfig.rootpath)
    build_dir = proj_path / "build" / "core" / "counter"

    run(
        verilog_sources=[
            proj_path / "src" / "core" / "counter" / "counter.sv"
        ],
        toplevel="counter",
        module="counter_cocotb",
        sim_build=build_dir,
        waves=True,
    )

    wavefile = build_dir / "dump.fst"
    if wavefile.exists():
        wavefile.rename(build_dir / "test_counter.fst")
