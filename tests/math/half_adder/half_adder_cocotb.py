import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_half_adder(dut):
    """ Half adder test. """

    # for i in range(2 ** 3):
    #     i_a = i & 1
    #     i_b = (i >> 1) & 1
    #     i_carry = (i >> 2) & 1
    #     o_sum = i_a ^ i_b ^ i_carry;
    #     o_carry = ((i_a | i_b) & i_carry) | (i_a & i_b);

    #     dut.i_a <= i_a
    #     dut.i_b <= i_b
    #     dut.i_carry <= i_carry
    #     await Timer(1)
    #     assert dut.o_sum == o_sum
    #     assert dut.o_carry == o_carry