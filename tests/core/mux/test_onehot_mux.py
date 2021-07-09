from cocotb_test.simulator import run
import os
from pathlib import Path


def test_onehot_mux(pytestconfig):
    """One-hot mux test."""

    os.environ["SIM"] = "verilator"
    proj_path = Path(pytestconfig.rootpath)
    build_dir = proj_path / "build" / "core" / "mux"

    run(
        verilog_sources=[proj_path / "src" / "core" / "mux" / "onehot_mux.sv"],
        toplevel="onehot_mux",
        module="onehot_mux_cocotb",
        sim_build=build_dir,
        waves=True,
    )

    wavefile = build_dir / "dump.fst"
    if wavefile.exists():
        wavefile.rename(build_dir / "test_onehot_mux.fst")
