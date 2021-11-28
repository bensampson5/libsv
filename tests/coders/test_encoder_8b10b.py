import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from typing import Tuple
import re
from utils import pytest_cocotb_run_test


def test_8b10b_encoder(pytestconfig):
    """Pytest fixture for 8B/10B Encoder test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


def encode_5b6b(i_5b: int, i_disp: int, i_ctrl: bool) -> Tuple[int, int]:
    """5b/6b encoder.

    Args:
        i_5b (int): input 5b value
        i_disp (int): input running disparity (-1 or 1)
        i_ctrl (bool): intput control symbol flag

    Returns:
        tuple[int, int]: tuple of output 6b value and output running disparity
    """

    # lookup table maps EDBCA to iedcba for RD = -1
    lut_5b6b_rdm1 = {
        # EDCBA:   iebcba
        0b00000: 0b111001,  # D.00-
        0b00001: 0b101110,  # D.01-
        0b00010: 0b101101,  # D.02-
        0b00011: 0b100011,  # D.03-
        0b00100: 0b101011,  # D.04-
        0b00101: 0b100101,  # D.05-
        0b00110: 0b100110,  # D.06-
        0b00111: 0b000111,  # D.07-
        0b01000: 0b100111,  # D.08-
        0b01001: 0b101001,  # D.09-
        0b01010: 0b101010,  # D.10-
        0b01011: 0b001011,  # D.11-
        0b01100: 0b101100,  # D.12-
        0b01101: 0b001101,  # D.13-
        0b01110: 0b001110,  # D.14-
        0b01111: 0b111010,  # D.15-
        0b10000: 0b110110,  # D.16-
        0b10001: 0b110001,  # D.17-
        0b10010: 0b110010,  # D.18-
        0b10011: 0b010011,  # D.19-
        0b10100: 0b110100,  # D.20-
        0b10101: 0b010101,  # D.21-
        0b10110: 0b010110,  # D.22-
        0b10111: 0b010111,  # D.23-
        0b11000: 0b110011,  # D.24-
        0b11001: 0b011001,  # D.25-
        0b11010: 0b011010,  # D.26-
        0b11011: 0b011011,  # D.27-
        0b11100: 0b001110,  # D.28-
        0b11101: 0b011101,  # D.29-
        0b11110: 0b011110,  # D.30-
        0b11111: 0b110101,  # D.31-
    }

    o_6b = lut_5b6b_rdm1[i_5b]  # lookup 5b/6b RD- value

    # K.28 is unique from the rest of the table
    if i_ctrl and i_5b == 28:
        if i_disp == -1:
            o_6b = 0b111100
        else:
            o_6b = 0b000011

    elif i_disp == 1:  # may have to look up RD+ value

        # check if RD+ value is different than RD- value
        if i_5b in [0, 1, 2, 4, 7, 8, 15, 16, 23, 24, 27, 29, 30, 31]:
            o_6b = (~o_6b) & 0x3F

    # update running disparity
    string_6b = format(o_6b, "06b")
    num_ones = string_6b.count("1")
    num_zeros = string_6b.count("0")
    o_disp = i_disp + num_ones - num_zeros

    # Check for invalid output running disparity
    try:
        assert o_disp == -1 or o_disp == 1
    except AssertionError as e:
        i_5b_str = format(i_5b, "#07b")
        o_6b_str = format(o_6b, "#08b")
        print(
            f"Error: Invalid output running disparity value\n"
            f"    i_5b = {i_5b_str}, i_disp = {i_disp}, i_ctrl = {i_ctrl}\n"
            f"    o_6b = {o_6b_str}, o_disp = {o_disp}\n"
        )
        raise e

    return o_6b, o_disp


def encode_3b4b(
    i_3b: int, i_disp: int, i_ctrl: bool, use_alternate: bool
) -> Tuple[int, int]:
    """3b/4b encoder.

    Args:
        i_3b (int): input 3b value
        i_disp (int): input running disparity (-1 or 1)
        i_ctrl (bool): input control symbol flag
        use_alternate (bool): Use alternate flag (for D.x.A7)

    Returns:
        tuple[int, int]: tuple of output 4b value and output running disparity
    """

    # lookup table maps HGF to jhgf for RD = -1 (data)
    lut_3b4b_data_rdm1 = {
        # HGF:   jhgf
        0b000: 0b1101,  # D.x.0-
        0b001: 0b1001,  # D.x.1-
        0b010: 0b1010,  # D.x.2-
        0b011: 0b0011,  # D.x.3-
        0b100: 0b1011,  # D.x.4-
        0b101: 0b0101,  # D.x.5-
        0b110: 0b0110,  # D.x.6-
        0b111: 0b0111,  # D.x.P7-
    }

    # lookup table maps HGF to jhgf for RD = -1 (control)
    lut_3b4b_control_rdm1 = {
        # HGF:   jhgf
        0b000: 0b1101,  # K.x.0-
        0b001: 0b0110,  # K.x.1-
        0b010: 0b0101,  # K.x.2-
        0b011: 0b0011,  # K.x.3-
        0b100: 0b1011,  # K.x.4-
        0b101: 0b1010,  # K.x.5-
        0b110: 0b1001,  # K.x.6-
        0b111: 0b1110,  # K.x.7-
    }

    # lookup 3b/4b RD- value
    o_4b = None
    if i_ctrl:
        o_4b = lut_3b4b_control_rdm1[i_3b]
    else:
        if use_alternate and i_3b == 0b111:
            o_4b = 0b1110  # RD- value for D.x.A7
        else:
            o_4b = lut_3b4b_data_rdm1[i_3b]

    # Invert bits to get RD+ value if needed
    if i_disp == 1 and (i_ctrl or i_3b in [0, 3, 4, 7]):
        o_4b = (~o_4b) & 0xF

    # update running disparity
    string_4b = format(o_4b, "04b")
    num_ones = string_4b.count("1")
    num_zeros = string_4b.count("0")
    o_disp = i_disp + num_ones - num_zeros

    # Check for invalid output running disparity
    try:
        assert o_disp == -1 or o_disp == 1
    except AssertionError as e:
        i_3b_str = format(i_3b, "#05b")
        o_4b_str = format(o_4b, "#06b")
        print(
            f"Error: Invalid output running disparity value\n"
            f"    i_3b = {i_3b_str}, i_disp = {i_disp}, i_ctrl = {i_ctrl}\n"
            f"    use_alternate = {use_alternate}\n"
            f"    o_4b = {o_4b_str}, o_disp = {o_disp}\n"
        )
        raise e

    return o_4b, o_disp


def encode_8b10b(i_8b: int, i_disp: int, i_ctrl: bool) -> Tuple[int, int, bool]:
    """8b/10b encoder.

    Args:
        i_8b (int): input 8b value
        i_disp (int): input running disparity (-1 or 1)
        i_ctrl (bool): input control symbol flag

    Returns:
        Tuple[int, int, bool]: Tuple containing output 10b value, output running
            disparity, and output code error flag
    """

    i_5b = i_8b & 0x1F
    i_3b = (i_8b >> 5) & 0x7

    # Step 1: Lookup 5b/6b code
    o_6b, o_disp_6b = encode_5b6b(i_5b, i_disp, i_ctrl)

    # Step 2: Select alternate 3b/4b encoding to avoid run of
    # five consecutive 0s or 1s when combined with the preceding
    # 5b/6b code. D.x.A7 is used only when:
    #    1. RD = -1: for x = 17, 18, and 20
    #    2. RD = +1: for x = 11, 13, and 14
    use_alternate = (o_disp_6b == -1 and i_5b in [17, 18, 20]) or (
        o_disp_6b == 1 and i_5b in [11, 13, 14]
    )

    # Step 3: Lookup 3b/4b code
    o_4b, o_disp_4b = encode_3b4b(i_3b, o_disp_6b, i_ctrl, use_alternate)

    # Combine 6b and 4b codes to a 10b code
    o_10b = (o_4b << 6) | o_6b
    o_disp = o_disp_4b

    try:
        # Check that there isn't a string of 0's or 1's longer than 5
        o_10b_s = format(o_10b, "010b")
        assert not re.search("0{6,}|1{6,}", o_10b_s)
    except AssertionError as e:
        i_8b_str = format(i_8b, "#05b")
        o_10b_str = format(o_10b, "#012b")
        print(
            f"Error: 10b value has a string of 0's or 1's longer than 5\n"
            f"    i_8b = {i_8b_str}, i_rd = {i_disp}, i_ctrl = {i_ctrl}\n"
            f"    use_alternate = {use_alternate}\n"
            f"    o_10b = {o_10b_str}, o_rd = {o_disp}\n"
        )
        raise e

    # Look up illegal codes
    o_code_err = False
    legal_control_symbols = [
        0b00011100,  # K.28.0
        0b00111100,  # K.28.1
        0b01011100,  # K.28.2
        0b01111100,  # K.28.3
        0b10011100,  # K.28.4
        0b10111100,  # K.28.5
        0b11011100,  # K.28.6
        0b11111100,  # K.28.7
        0b11110111,  # K.23.7
        0b11111011,  # K.27.7
        0b11111101,  # K.29.7
        0b11111110,  # K.30.7
    ]
    if i_ctrl and i_8b not in legal_control_symbols:
        o_code_err = True

    return o_10b, o_disp, o_code_err


@cocotb.test()
async def cocotb_test_encoder_8b10b(dut):
    """8B/10B Encoder test"""

    # Create clock
    cocotb.fork(Clock(dut.i_clk, 2).start())

    # Assert reset and check output and
    # internal running disparity
    dut.i_reset_n.value = 0
    await FallingEdge(dut.i_clk)
    assert int(dut.o_10b) == 0
    assert int(dut.o_code_err) == 0
    assert int(dut.rd) == 0

    # Check that enable doesn't change outputs when disabled
    dut.i_reset_n.value = 1  # de-assert reset
    dut.i_en.value = 1  # enable 8b10b encoder
    dut.i_8b.value = 0  # D.00.0
    dut.i_ctrl.value = 0  # data symbol
    await FallingEdge(dut.i_clk)  # 1 clock tick
    prev_o_10b = int(dut.o_10b)  # capture 10b output
    prev_o_code_err = int(dut.o_code_err)  # capture code error
    prev_rd = int(dut.rd)  # capture running disparity
    dut.i_en.value = 0  # disable 8b10b encoder

    # Pick a value that after the first 8b value would change both
    # the output 10b value, internal running disparity, and generate
    # a code error
    dut.i_ctrl.value = 1  # control symbol
    dut.i_8b.value = 0b00000011  # K.03.0

    await FallingEdge(dut.i_clk)  # 1 clock tick
    assert prev_o_10b == int(dut.o_10b)  # output should not have changed
    assert prev_o_code_err == int(dut.o_code_err)  # code error should not have changed
    assert prev_rd == int(dut.rd)  # running disparity should not have changed

    # Test 8b/10b encoding look-up table
    dut.i_reset_n.value = 1
    dut.i_en.value = 1
    for i in range(2 ** 10):

        # Parse out input values
        i_8b = i & 0xFF
        i_disp = (i >> 8) & 1
        i_ctrl = (i >> 9) & 1

        # Run the software 8b10b encoder
        py_i_8b = i_8b
        py_i_disp = (i_disp * 2) - 1
        py_i_ctrl = bool(i_ctrl)
        py_o_10b, py_o_disp, py_o_code_err = encode_8b10b(py_i_8b, py_i_disp, py_i_ctrl)

        # Calculate expected dut outputs using software
        # 8b/10b encoder results
        o_10b = py_o_10b
        o_disp = (py_o_disp + 1) // 2
        o_code_err = int(py_o_code_err)

        # Push inputs to dut
        dut.i_8b.value = i_8b
        dut.i_ctrl.value = i_ctrl

        # Force internal running disparity to specific value
        dut.rd.value = i_disp

        d_prev_rd = int(dut.rd)  # save previous RD value

        # Step 1 clock tick
        await FallingEdge(dut.i_clk)  # 1 clock tick

        # Check actual outputs vs expected outputs
        try:
            assert int(dut.o_10b) == o_10b
            assert int(dut.rd) == o_disp
            assert int(dut.o_code_err) == o_code_err
        except AssertionError as e:
            i_8b_s = format(i_8b, "#010b")
            i_ctrl_s = format(i_ctrl, "#03b")
            d_i_8b_s = "0b" + str(dut.i_8b.value)
            d_i_ctrl_s = "0b" + str(dut.i_ctrl.value)
            d_prev_rd_s = format(d_prev_rd, "#03b")
            d_rd_s = "0b" + str(dut.rd.value)
            d_o_10b_s = "0b" + str(dut.o_10b.value)
            d_o_code_err_s = "0b" + str(dut.o_code_err.value)
            o_10b_s = format(o_10b, "#012b")
            o_code_err_s = format(o_code_err, "#03b")
            print(
                f"Error: Actual outputs do not match expected outputs\n"
                f"    i_8b      =   {i_8b_s}, i_ctrl         = {i_ctrl_s}\n"
                f"    dut.i_8b  =   {d_i_8b_s}, dut.i_ctrl     = {d_i_ctrl_s}\n"
                f"    previous dut.rd =    {d_prev_rd_s}, current dut.rd = {d_rd_s}\n"
                f"    dut.o_10b = {d_o_10b_s}, dut.o_code_err = {d_o_code_err_s}\n"
                f"    o_10b     = {o_10b_s}, o_code_err     = {o_code_err_s}\n"
            )
            raise e
