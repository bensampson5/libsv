import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from typing import Tuple
from utils import pytest_cocotb_run_test


def test_8b10b_decoder(pytestconfig):
    """Pytest fixture for 8B/10B Decoder test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


def decode_5b6b(i_6b: int, i_disp: int) -> Tuple[int, int, bool, bool]:
    """5b/6b decoder.

    Args:
        i_6b (int): input 6b value
        i_disp (int): input disparity (-1 or 1)

    Returns:
        tuple[int, int, bool, bool]: tuple of output 5b value, output disparity,
            control symbol flag, code error flag, and disparity error flag
    """

    # lookup table maps iedcba to EDBCA
    lut_6b5b = {
        # iebcba:   EDCBA
        0b000000: None,  # Illegal code
        0b000001: None,  # Illegal code
        0b000010: None,  # Illegal code
        0b000011: 0b11100,  # K.28+
        0b000100: None,  # Illegal code
        0b000101: 0b01111,  # D.15+
        0b000110: 0b00000,  # D.0+
        0b000111: 0b00111,  # D.7-
        0b001000: None,  # Illegal code
        0b001001: 0b10000,  # D.16+
        0b001010: 0b11111,  # D.31+
        0b001011: 0b01011,  # D.11
        0b001100: 0b11000,  # D.24+
        0b001101: 0b01101,  # D.13
        0b001110: 0b01110,  # D.14
        0b001111: None,  # Illegal code (not used)
        0b010000: None,  # Illegal code
        0b010001: 0b00001,  # D.01+
        0b010010: 0b00010,  # D.02+
        0b010011: 0b10011,  # D.19
        0b010100: 0b00100,  # D.04+
        0b010101: 0b10101,  # D.21
        0b010110: 0b10110,  # D.22
        0b010111: 0b10111,  # D.23-
        0b011000: 0b01000,  # D.08+
        0b011001: 0b11001,  # D.25
        0b011010: 0b11010,  # D.26
        0b011011: 0b11011,  # D.27-
        0b011100: 0b11100,  # D.28
        0b011101: 0b11101,  # D.29-
        0b011110: 0b11110,  # D.30-
        0b011111: None,  # Illegal code
        0b100000: None,  # Illegal code
        0b100001: 0b11110,  # D.30+
        0b100010: 0b11101,  # D.29+
        0b100011: 0b00011,  # D.03
        0b100100: 0b11011,  # D.27+
        0b100101: 0b00101,  # D.05
        0b100110: 0b00110,  # D.06
        0b100111: 0b01000,  # D.08-
        0b101000: 0b10111,  # D.23+
        0b101001: 0b01001,  # D.09
        0b101010: 0b01010,  # D.10
        0b101011: 0b00100,  # D.04-
        0b101100: 0b01100,  # D.12
        0b101101: 0b00010,  # D.02-
        0b101110: 0b00001,  # D.01-
        0b101111: None,  # Illegal code
        0b110000: None,  # Illegal code (not used)
        0b110001: 0b10001,  # D.17
        0b110010: 0b10010,  # D.18
        0b110011: 0b11000,  # D.24-
        0b110100: 0b10100,  # D.20
        0b110101: 0b11111,  # D.31-
        0b110110: 0b10000,  # D.16-
        0b110111: None,  # Illegal code
        0b111000: 0b00111,  # D.07+
        0b111001: 0b00000,  # D.00-
        0b111010: 0b01111,  # D.15-
        0b111011: None,  # Illegal code
        0b111100: 0b11100,  # K.28-
        0b111101: None,  # Illegal code
        0b111110: None,  # Illegal code
        0b111111: None,  # Illegal code
    }

    o_5b = lut_6b5b[i_6b]  # lookup 5b/6b value
    o_disp = 0  # initialize output disparity
    o_code_err = False  # initialize code error flag
    o_disp_err = False  # initialize disparity error flag

    if o_5b is None:  # check if illegal code
        o_code_err = True
        o_5b = 0

    # calculate the output disparity
    string_6b = format(i_6b, "06b")
    num_ones = string_6b.count("1")
    num_zeros = string_6b.count("0")
    codeword_disp = num_ones - num_zeros

    if codeword_disp != 0:

        # regardless of whether there is a disparity error or not
        # the output disparity should always get flipped if it's
        # not equal to zero
        o_disp = -i_disp

        # Check for disparity error
        if (
            codeword_disp >= 3
            or codeword_disp <= -3
            or (i_disp == -1 and codeword_disp == -2)
            or (i_disp == 1 and codeword_disp == 2)
        ):
            o_disp_err = True

    else:  # if codeword disparity is 0 then output disparity is the input disparity
        o_disp = i_disp

    return o_5b, o_disp, o_code_err, o_disp_err


def decode_3b4b(i_4b: int, i_disp: int, i_ctrl: bool) -> Tuple[int, int]:
    """3b/4b decoder.

    Args:
        i_4b (int): input 4b value
        i_disp (int): input disparity (-1 or 1)
        i_ctrl (bool): input control symbol flag

    Returns:
        tuple[int, int]: tuple of output 3b value and output disparity
    """

    # lookup table maps jhgf to HGF
    lut_4b3b_data = {
        # jhgf:   HGF
        0b0000: None,  # Illegal code
        0b0001: 0b111,  # D.x.A7+
        0b0010: 0b000,  # D.x.0+
        0b0011: 0b011,  # D.x.3-
        0b0100: 0b100,  # D.x.4+
        0b0101: 0b101,  # D.x.5
        0b0110: 0b110,  # D.x.6
        0b0111: 0b111,  # D.x.P7-
        0b1000: 0b111,  # D.x.P7+
        0b1001: 0b001,  # D.x.1
        0b1010: 0b010,  # D.x.2
        0b1011: 0b100,  # D.x.4-
        0b1100: 0b011,  # D.x.3+
        0b1101: 0b000,  # D.x.0-
        0b1110: 0b111,  # D.x.A7-
        0b1111: None,  # Illegal code
    }

    lut_4b3b_control = {
        # jhgf:   HGF
        0b0000: None,  # Illegal code
        0b0001: 0b111,  # K.x.7+
        0b0010: 0b000,  # K.x.0+
        0b0011: 0b011,  # K.x.3-
        0b0100: 0b100,  # K.x.4+
        0b0101: -1,  # K.x.5+ / K.x.2- (must be handled using input disparity)
        0b0110: -1,  # K.x.6+ / K.x.1- (must be handled using input disparity)
        0b0111: None,  # Illegal code
        0b1000: None,  # Illegal code
        0b1001: -1,  # K.x.6- / K.x.1+ (must be handled using input disparity)
        0b1010: -1,  # K.x.5- / K.x.2+ (must be handled using input disparity)
        0b1011: 0b100,  # K.x.4-
        0b1100: 0b011,  # K.x.3+
        0b1101: 0b000,  # K.x.0-
        0b1110: 0b111,  # K.x.7-
        0b1111: None,  # Illegal code
    }

    # lookup 3b/4b value
    o_3b = 0
    if i_ctrl:
        o_3b = lut_4b3b_control[i_4b]

        if i_4b == 0b0101:  # check weird case #1
            if i_disp == -1:
                o_3b = 0b010  # K.x.2-
            else:
                o_3b = 0b101  # K.x.5+
        elif i_4b == 0b0110:  # check weird case #2
            if i_disp == -1:
                o_3b = 0b001  # K.x.1-
            else:  # K.x.6+
                o_3b = 0b110
        elif i_4b == 0b1001:  # check weird case #3
            if i_disp == -1:
                o_3b = 0b110  # K.x.6-
            else:
                o_3b = 0b001  # K.x.1+
        elif i_4b == 0b1010:  # check weird case #4
            if i_disp == -1:
                o_3b = 0b101  # K.x.5-
            else:
                o_3b = 0b010  # K.x.2+
    else:
        o_3b = lut_4b3b_data[i_4b]

    o_disp = 0  # initialize output disparity
    o_code_err = False  # initialize code error flag
    o_disp_err = False  # initialize disparity error flag

    if o_3b is None:  # check if illegal code
        o_code_err = True
        o_3b = 0

    # calculate the output disparity
    string_4b = format(i_4b, "04b")
    num_ones = string_4b.count("1")
    num_zeros = string_4b.count("0")
    codeword_disp = num_ones - num_zeros

    if codeword_disp != 0:

        # regardless of whether there is a disparity error or not
        # the output disparity should always get flipped if it's
        # not equal to zero
        o_disp = -i_disp

        # Check for disparity error
        if (
            codeword_disp >= 3
            or codeword_disp <= -3
            or (i_disp == -1 and codeword_disp == -2)
            or (i_disp == 1 and codeword_disp == 2)
        ):
            o_disp_err = True

    else:  # if codeword disparity is 0 then output disparity is the input disparity
        o_disp = i_disp

    return o_3b, o_disp, o_code_err, o_disp_err


def decode_8b10b(i_10b, i_disp):

    # Determine if control symbol
    control_symbols_rdm1 = [
        # jhgfiedcba
        0b0010111100,  # K.28.0-
        0b1001111100,  # K.28.1-
        0b1010111100,  # K.28.2-
        0b1100111100,  # K.28.3-
        0b0100111100,  # K.28.4-
        0b0101111100,  # K.28.5-
        0b0110111100,  # K.28.6-
        0b0001111100,  # K.28.7-
        0b0001010111,  # K.23.7-
        0b0001011011,  # K.27.7-
        0b0001011101,  # K.29.7-
        0b0001011110,  # K.30.7-
    ]
    control_symbols = control_symbols_rdm1 + [
        (~s) & 0x3FF for s in control_symbols_rdm1
    ]
    is_ctrl = i_10b in control_symbols

    # Parse out 6b and 4b inputs
    i_6b = i_10b & 0x3F
    i_4b = (i_10b >> 6) & 0xF

    # Decode 6b
    o_5b, o_disp_5, o_code_err_5, o_disp_err_5 = decode_5b6b(i_6b, i_disp)

    # Decode 4b
    o_3b, o_disp_3, o_code_err_3, o_disp_err_3 = decode_3b4b(i_4b, o_disp_5, is_ctrl)

    o_8b = (o_3b << 5) | o_5b
    o_disp = o_disp_3
    o_ctrl = is_ctrl
    o_code_err = o_code_err_3 | o_code_err_5
    o_disp_err = o_disp_err_3 | o_disp_err_5

    return o_8b, o_disp, o_ctrl, o_code_err, o_disp_err


@cocotb.test()
async def cocotb_test_decoder_8b10b(dut):
    """8B/10B Decoder test"""

    # Create clock
    cocotb.start_soon(Clock(dut.i_clk, 2).start())

    # Assert reset and check output and
    # internal running disparity
    dut.i_reset_n.value = 0
    await FallingEdge(dut.i_clk)
    assert int(dut.o_8b) == 0
    assert int(dut.o_ctrl) == 0
    assert int(dut.o_code_err) == 0
    assert int(dut.o_disp_err) == 0
    assert int(dut.rd) == 0

    # Check that enable doesn't change outputs when disabled
    dut.i_reset_n.value = 1  # de-assert reset
    dut.i_en.value = 1  # enable 8b10b decoder
    dut.i_10b.value = 0b1001001101  # D.13.1
    await FallingEdge(dut.i_clk)  # 1 clock tick
    prev_o_8b = int(dut.o_8b)  # capture 8b output
    prev_o_ctrl = int(dut.o_ctrl)  # capture control symbol flag
    prev_o_code_err = int(dut.o_code_err)  # capture code error
    prev_o_disp_err = int(dut.o_disp_err)  # capture disparity error
    prev_rd = int(dut.rd)  # capture running disparity
    dut.i_en.value = 0  # disable 8b10b decoder

    # Pick a value that after the first 10b value would change both
    # the output 8b value, internal running disparity, and generate
    # both a code error and disparity error
    dut.i_10b.value = 0b0000000111  # Illegal code

    await FallingEdge(dut.i_clk)  # 1 clock tick
    assert prev_o_8b == int(dut.o_8b)  # output should not have changed
    assert prev_o_ctrl == int(dut.o_ctrl)  # control flag should not have changed
    assert prev_o_code_err == int(dut.o_code_err)  # code error should not have changed
    assert prev_o_disp_err == int(dut.o_disp_err)  # disp error should not have changed
    assert prev_rd == int(dut.rd)  # running disparity should not have changed

    # Test 8b/10b decoding look-up table
    dut.i_reset_n.value = 1
    dut.i_en.value = 1
    for i in range(2 ** 11):

        # Parse out input values
        i_10b = i & 0x3FF
        i_disp = (i >> 10) & 1

        # Run the software 8b10b encoder
        py_i_10b = i_10b
        py_i_disp = (i_disp * 2) - 1
        py_o_8b, py_o_disp, py_o_ctrl, py_o_code_err, py_o_disp_err = decode_8b10b(
            py_i_10b, py_i_disp
        )

        # Calculate expected dut outputs using software
        # 8b/10b decoder results
        o_8b = py_o_8b
        o_ctrl = int(py_o_ctrl)
        o_code_err = int(py_o_code_err)
        o_disp_err = int(py_o_disp_err)

        # Push input to dut
        dut.i_10b.value = i_10b

        # Force internal running disparity to specific value
        dut.rd.value = i_disp

        d_prev_rd = int(dut.rd)  # save previous RD value

        # Step 1 clock tick
        await FallingEdge(dut.i_clk)  # 1 clock tick

        # Check actual outputs vs expected outputs
        try:
            assert int(dut.o_8b) == o_8b
            assert int(dut.o_ctrl) == o_ctrl
            assert int(dut.o_code_err) == o_code_err
            assert int(dut.o_disp_err) == o_disp_err
        except AssertionError as e:
            i_10b_s = format(i_10b, "#012b")
            d_i_10b_s = "0b" + str(dut.i_10b.value)
            d_prev_rd_s = format(d_prev_rd, "#03b")
            d_rd_s = "0b" + str(dut.rd.value)
            d_o_8b_s = "0b" + str(dut.o_8b.value)
            d_o_ctrl_s = "0b" + str(dut.o_ctrl.value)
            d_o_code_err_s = "0b" + str(dut.o_code_err.value)
            d_o_disp_err_s = "0b" + str(dut.o_disp_err.value)
            d_o_code_err_s = "0b" + str(dut.o_code_err.value)
            o_8b_s = format(o_8b, "#010b")
            o_ctrl_s = format(o_ctrl, "#03b")
            o_code_err_s = format(o_code_err, "#03b")
            o_disp_err_s = format(o_disp_err, "#03b")

            print(
                f"Error: Actual outputs do not match expected outputs\n"
                f"    i_10b     = {i_10b_s}\n"
                f"    dut.i_10b = {d_i_10b_s}\n"
                f"    dut.o_8b  =   {d_o_8b_s}, dut.o_ctrl = {d_o_ctrl_s}, "
                f"dut.o_code_err = {d_o_code_err_s}, "
                f"dut.o_disp_err = {d_o_disp_err_s}\n"
                f"    previous dut.rd =    {d_prev_rd_s}, current dut.rd = {d_rd_s}\n"
                f"    o_8b      =   {o_8b_s}, o_ctrl     = {o_ctrl_s}, "
                f"o_code_err     = {o_code_err_s}, "
                f"o_disp_err     = {o_disp_err_s}\n"
            )
            raise e
