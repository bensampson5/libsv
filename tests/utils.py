import os
from pathlib import Path
from cocotb_test.simulator import run


def pytest_cocotb_run_test(pytestconfig, test_name):
    os.environ["SIM"] = "verilator"  # always use verilator as HDL simulator
    proj_path = Path(pytestconfig.rootpath)  # capture top-level project path

    # get top level module name from file test name
    top_level = test_name.replace("test_", "")

    # determine verilog sources from top_level module
    src_dir = proj_path / "libsv"
    top_level_sv = list(src_dir.glob(f"**/{top_level}.sv"))
    if len(top_level_sv) == 1:
        top_level_sv = top_level_sv[0]
        with open(top_level_sv, "r") as f:

            found_top_level_module = False
            while not found_top_level_module:
                line = f.readline()
                if line.startswith(f"module {top_level} "):
                    found_top_level_module = True

        if not found_top_level_module:
            raise RuntimeError("Could not find top level module")
    else:
        raise RuntimeError("Too many sv top level files")

    # determine build directory
    build_dir = Path(str(top_level_sv.parent).replace("libsv", "build"))

    # call to cocotb_test.simulator.run
    run(
        verilog_sources=[top_level_sv],
        toplevel=top_level,
        module=test_name,
        includes=[proj_path],
        sim_build=build_dir,
        waves=True,
    )

    # rename waveform file
    wavefile = build_dir / "dump.fst"
    if wavefile.exists():
        wavefile.rename(build_dir / f"{test_name}.fst")
