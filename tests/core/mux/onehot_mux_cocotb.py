import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def test_onehot_mux(dut):
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
