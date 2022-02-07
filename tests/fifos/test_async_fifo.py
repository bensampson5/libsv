import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from utils import pytest_cocotb_run_test


def test_async_fifo(pytestconfig):
    """Pytest fixture for Async Fifo test"""
    pytest_cocotb_run_test(pytestconfig, __name__)


@cocotb.test()
async def cocotb_test_async_fifo(dut):
    """Async Fifo test"""

    data_width = int(dut.DATA_WIDTH)
    fifo_depth = int(dut.FIFO_DEPTH)

    cocotb.fork(Clock(dut.i_wr_clock, 2).start())
    cocotb.fork(Clock(dut.i_rd_clock, 2).start())

    # reset
    dut.i_aresetn.value = 0
    await FallingEdge(dut.i_wr_clock)
    dut.i_aresetn.value = 1

    # fill up fifo completely
    dut.i_wr_en.value = 1
    for i in range(1, fifo_depth + 1):
        dut.i_data.value = i % data_width
        await FallingEdge(dut.i_wr_clock)

    assert int(dut.o_full.value) == 1

    # # read out everything from fifo completely
    # dut.i_wr_en.value = 0
    # dut.i_rd_en.value = 1
    # for i in range(1, fifo_depth + 1):
    #     assert int(dut.o_data.value) == i % data_width
    #     await FallingEdge(dut.i_wr_clock)

    # assert int(dut.o_full.value) == 0
    # assert int(dut.o_empty.value) == 1

    # #  test streaming with 1 entry in fifo
    # for i in range(1, 6):
    #     if i == 1:
    #         dut.i_wr_en.value = 1
    #         dut.i_data.value = i % data_width
    #         await FallingEdge(dut.i_wr_clock)
    #         dut.i_rd_en.value = 1
    #     else:
    #         assert int(dut.o_data.value) == (i - 1) % data_width
    #         dut.i_data.value = i % data_width
    #         await FallingEdge(dut.i_wr_clock)

    #     assert int(dut.o_empty.value) == 0  # never is empty

    # # test streaming with fifo_depth-1 entries in fifo
    # dut.i_wr_en.value = 1
    # dut.i_rd_en.value = 0
    # dut.i_aresetn.value = 0
    # await FallingEdge(dut.i_wr_clock)
    # dut.i_aresetn.value = 1
    # for i in range(1, fifo_depth + 5):
    #     if i < fifo_depth:  # fill up fifo
    #         dut.i_data.value = i % data_width
    #         await FallingEdge(dut.i_wr_clock)
    #         if i == fifo_depth - 1:
    #             dut.i_rd_en.value = 1
    #     else:
    #         assert int(dut.o_data.value) == (i - (fifo_depth - 1)) % data_width
    #         dut.i_data.value = i % data_width
    #         await FallingEdge(dut.i_wr_clock)

    #     assert int(dut.o_full.value) == 0  # never is full
