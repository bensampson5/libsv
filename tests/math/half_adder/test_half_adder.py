from cocotb_test.simulator import run
import os
from pathlib import Path
import cocotb
from cocotb.triggers import Timer


def test_half_adder(pytestconfig):

    os.environ["SIM"] = "verilator"
    proj_path = Path(pytestconfig.rootpath)
    build_dir = proj_path / "build" / "math" / "half_adder"

    run(
        verilog_sources=[proj_path / "src" / "math" / "half_adder" / "half_adder.sv"],
        toplevel="half_adder",
        module="test_half_adder",
        sim_build=build_dir,
        waves=True,
    )

    wavefile = build_dir / "dump.fst"
    if wavefile.exists():
        wavefile.rename(build_dir / "test_half_adder.fst")


@cocotb.test()
async def cocotb_test_half_adder(dut):
    """Half adder test."""

    for i in range(2 ** 2):
        i_a = i & 1
        i_b = (i >> 1) & 1
        o_sum = i_a ^ i_b
        o_carry = i_a & i_b

        dut.i_a <= i_a
        dut.i_b <= i_b
        await Timer(1)
        assert dut.o_sum == o_sum
        assert dut.o_carry == o_carry
