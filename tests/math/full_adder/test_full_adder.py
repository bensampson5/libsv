from cocotb_test.simulator import run
import os
from pathlib import Path
import cocotb
from cocotb.triggers import Timer


def test_full_adder(pytestconfig):
    """Full adder test."""

    os.environ["SIM"] = "verilator"
    proj_path = Path(pytestconfig.rootpath)
    build_dir = proj_path / "build" / "math" / "full_adder"

    run(
        verilog_sources=[proj_path / "src" / "math" / "full_adder" / "full_adder.sv"],
        toplevel="full_adder",
        module="test_full_adder",
        sim_build=build_dir,
        waves=True,
    )

    wavefile = build_dir / "dump.fst"
    if wavefile.exists():
        wavefile.rename(build_dir / "test_full_adder.fst")


@cocotb.test()
async def cocotb_test_full_adder(dut):
    """Full adder test."""

    for i in range(2 ** 3):
        i_a = i & 1
        i_b = (i >> 1) & 1
        i_carry = (i >> 2) & 1
        o_sum = i_a ^ i_b ^ i_carry
        o_carry = ((i_a | i_b) & i_carry) | (i_a & i_b)

        dut.i_a <= i_a
        dut.i_b <= i_b
        dut.i_carry <= i_carry
        await Timer(1)
        assert dut.o_sum == o_sum
        assert dut.o_carry == o_carry
