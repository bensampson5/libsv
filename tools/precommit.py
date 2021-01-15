#!/usr/bin/env python

import sys
from pathlib import Path
import shutil
import argparse
import errno
import subprocess

PROJECT_ROOT = Path("/code")
BUILD_DIR = PROJECT_ROOT / "build"

def in_docker():
    """ Returns: True if runnning in a docker container, else False """
    try:
        with open("/proc/1/cgroup", "rt") as ifh:
            return "docker" in ifh.read()
    except:
        return False

def run(cmd, cwd=PROJECT_ROOT, check_exit=True):
    try:
        exit_code = subprocess.call(cmd, cwd=cwd)

        if check_exit and exit_code != 0:
            print(f"{' '.join(cmd)} exited with non-zero {exit_code}")
    except OSError as e:
        if e.errno == errno.ENOENT:
            print(f"Command {cmd[0]} not found")
            raise e
        else:
            raise e

def cmake(flags=["-GNinja"]):
    
    # Delete entire build directory if it exists
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    # Create new build directory
    BUILD_DIR.mkdir()

    # Create cmake command
    cmd = ["cmake"]
    if flags is not None:
        cmd += flags
    cmd += [".."]

    run(cmd, cwd=BUILD_DIR)

def build(flags=None, cwd=BUILD_DIR):

    if not cwd.exists():
        raise FileNotFoundError("Could not find build directory to run build")

    cmd = ["ninja"]
    if flags is not None:
        cmd += flags

    run(cmd, cwd=cwd)

def test():

    if not BUILD_DIR.exists():
        raise FileNotFoundError("Could not find build directory to run tests")

    cmd = ["ninja", "check"]

    run(cmd, cwd=BUILD_DIR)

def format():
    format_hdl()

def format_hdl():
    src_dir = PROJECT_ROOT / "src"

    if not src_dir.exists():
        raise FileNotFoundError("Could not find src directory to format HDL")

    cmd = ["verible-verilog-format", "--inplace"]

    # Add options from .verible-verilog-format if specified
    verible_verilog_format_file = PROJECT_ROOT / ".verible-verilog-format"
    format_args = []
    if verible_verilog_format_file.exists():
        with open(verible_verilog_format_file, "r") as f:
            for line in f:
                if line[0] != "#" and len(line.rstrip()) > 0: # ignore comments and empty lines
                    format_args.append(line.rstrip())
    cmd += format_args

    # Add all SystemVerilog or Verilog files in src directory
    hdl_search_patterns = ["**/*.sv", "**/*.v"]
    hdl_files = []
    for sp in hdl_search_patterns:
        hdl_files += src_dir.glob(sp)
    cmd += [str(f) for f in hdl_files]

    run(cmd)

if __name__ == "__main__":
    if not in_docker():
        raise OSError("Not in a docker container. This script must be run from within a docker container. See README.md for instructions.")
    else:

        # Resolve project root directory before proceeding
        if not PROJECT_ROOT.is_dir():
            raise FileNotFoundError(f"Cannot find project root directory: {PROJECT_ROOT}")

        parser = argparse.ArgumentParser()
        arg_list = ["--skip-build", "--skip-test", "--skip-format"]
        for arg in arg_list:
            parser.add_argument(arg, action="store_true")
        args = parser.parse_args()

        if not args.skip_build:
            print("Building...")
            cmake()
            build()

            if not args.skip_test:
                print("Testing...")
                test()
        
        if not args.skip_format:
            print("Formatting...")
            format()