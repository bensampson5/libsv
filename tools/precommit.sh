#!/bin/bash
# Note: Should be run from project root directory

# Format all SystemVerilog/Verilog files
verible-verilog-format --inplace $(find . -type f  \( -name "*.sv" -o -name "*.v" \))