import cocotb
from cocotb.triggers import Timer
from typing import Tuple
from utils import pytest_cocotb_run_test


def test_5b6b_encoder(pytestconfig):
    """Pytest fixture for BCD Encoder test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


# 5b/6b encoding table
# Format is REDCBA : riedbca where R is the input running
# disparity, and r is the output running disparity
dict_5b6b = {
    0b000000: 0b1111001,  # D.00-
    0b000001: 0b1101110,  # D.01-
    0b000010: 0b1101101,  # D.02-
    0b000011: 0b0100011,  # D.03-
    0b000100: 0b1101011,  # D.04-
    0b000101: 0b0100101,  # D.05-
    0b000110: 0b0100110,  # D.06-
    0b000111: 0b1000111,  # D.07-
    0b001000: 0b1100111,  # D.08-
    0b001001: 0b0101001,  # D.09-
    0b001010: 0b0101010,  # D.10-
    0b001011: 0b0001011,  # D.11-
    0b001100: 0b0101100,  # D.12-
    0b001101: 0b0001101,  # D.13-
    0b001110: 0b0001110,  # D.14-
    0b001111: 0b1111010,  # D.15-
    0b010000: 0b1110110,  # D.16-
    0b010001: 0b0110001,  # D.17-
    0b010010: 0b0110010,  # D.18-
    0b010011: 0b0010011,  # D.19-
    0b010100: 0b0110100,  # D.20-
    0b010101: 0b0010101,  # D.21-
    0b010110: 0b0010110,  # D.22-
    0b010111: 0b1010111,  # D.23-
    0b011000: 0b1110011,  # D.24-
    0b011001: 0b0011001,  # D.25-
    0b011010: 0b0011010,  # D.26-
    0b011011: 0b1011011,  # D.27-
    0b011100: 0b0011100,  # D.28-
    0b011101: 0b1011101,  # D.29-
    0b011110: 0b1011110,  # D.30-
    0b011111: 0b1110101,  # D.31-
    0b100000: 0b0000110,  # D.00+
    0b100001: 0b0010001,  # D.01+
    0b100010: 0b0010010,  # D.02+
    0b100011: 0b1100011,  # D.03+
    0b100100: 0b0010100,  # D.04+
    0b100101: 0b1100101,  # D.05+
    0b100110: 0b1100110,  # D.06+
    0b100111: 0b0111000,  # D.07+
    0b101000: 0b0011000,  # D.08+
    0b101001: 0b1101001,  # D.09+
    0b101010: 0b1101010,  # D.10+
    0b101011: 0b1001011,  # D.11+
    0b101100: 0b1101100,  # D.12+
    0b101101: 0b1001101,  # D.13+
    0b101110: 0b1001110,  # D.14+
    0b101111: 0b0000101,  # D.15+
    0b110000: 0b0001001,  # D.16+
    0b110001: 0b1110001,  # D.17+
    0b110010: 0b1110010,  # D.18+
    0b110011: 0b1010011,  # D.19+
    0b110100: 0b1110100,  # D.20+
    0b110101: 0b1010101,  # D.21+
    0b110110: 0b1010110,  # D.22+
    0b110111: 0b0101000,  # D.23+
    0b111000: 0b0001100,  # D.24+
    0b111001: 0b1011001,  # D.25+
    0b111010: 0b1011010,  # D.26+
    0b111011: 0b0100100,  # D.27+
    0b111100: 0b1011100,  # D.28+
    0b111101: 0b0100010,  # D.29+
    0b111110: 0b0100001,  # D.30+
    0b111111: 0b0001010,  # D.31+
}


def encode_5b6b(i_5b: int, i_rd: int, i_is_control: int) -> Tuple[int, int]:
    """5b/6b encoding function that uses look-up tables. Calculates output 6b
    value and running display based on input 5b value, input running disparity,
    and input control symbol flag.

    Args:
        i_5b (int): input 5b value
        i_rd (int): input running disparity (0 or 1)
        i_is_control (int): input is control symbol flag (0 or 1)

    Returns:
        tuple[int, int]: tuple of output 6b value and output running disparity
    """

    if i_is_control == 1 and i_5b == 0b11100:  # K.28
        if i_rd:
            return 0b000011, 0
        else:
            return 0b111100, 1

    i_lookup = (i_rd << 5) | i_5b
    o_lookup = dict_5b6b[i_lookup]

    return o_lookup & 0x3F, o_lookup >> 6


@cocotb.test()
async def cocotb_test_encoder_5b6b(dut):
    """5B/6B Encoder test"""

    for i_vector in range(2 ** 7):

        i_5b = i_vector & 0x1F
        dut.i_5b.value = i_5b

        i_rd = (i_vector >> 5) & 0x1
        dut.i_rd.value = i_rd

        i_is_control = (i_vector >> 6) & 0x1
        dut.i_is_control.value = i_is_control

        o_6b, o_rd = encode_5b6b(i_5b, i_rd, i_is_control)
        await Timer(1)

        try:
            assert int(dut.o_6b) == o_6b
            assert int(dut.o_rd) == o_rd
        except AssertionError as e:
            print(
                f"Failed: i_5b = {format(i_5b, '#07b')}, i_rd = {format(i_rd, '#03b')},"
                f" i_is_control = {format(i_is_control, '#03b')}\n"
                f"        dut.i_5b = 0b{dut.i_5b.value}, dut.i_rd = 0b{dut.i_rd.value},"
                f" dut.i_is_control = 0b{dut.i_is_control.value}\n"
                f"        dut.o_6b = 0b{dut.o_6b.value}, dut.o_rd = 0b{dut.o_rd.value}"
                f"\n"
                f"        o_6b = {format(o_6b, '#08b')}, o_rd = {format(o_rd, '#03b')}"
                f"\n"
            )
            raise e
