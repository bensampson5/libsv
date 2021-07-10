#!/usr/bin/env python3

import click
from pathlib import Path
import shutil
import subprocess
import colorama
import yaml
from difflib import unified_diff
from colorama import Fore, Style

PROJECT_ROOT = Path("/code")
SRC_DIR = PROJECT_ROOT / "src"
DOCS_DIR = PROJECT_ROOT / "docs"
FLUSH = True


def in_docker():
    """Returns: True if running in a docker container, else False"""
    try:
        with open("/proc/1/cgroup", "rt") as ifh:
            contents = ifh.read()
            return any([word in contents for word in ["actions_job", "docker"]])
    except OSError:
        return False


def run(cmd, cwd=PROJECT_ROOT, check_exit=True, print_output=True):
    p = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )

    output = ""
    while True:
        stdout = p.stdout.readline()
        if stdout == "" and p.poll() is not None:
            break
        if stdout:
            if print_output:
                print(stdout, end="", flush=FLUSH)

    if check_exit and p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, " ".join(cmd))


def run_test():
    """Run tests"""
    cmd = ["pytest"]
    run(cmd)


def find_project_hdl_files(dir=SRC_DIR):
    # Add all SystemVerilog or Verilog files within project
    hdl_search_patterns = ["**/*.sv", "**/*.v"]
    hdl_files = []
    for sp in hdl_search_patterns:
        hdl_files += dir.glob(sp)
    return hdl_files


def run_check_format():
    """Check formatting in all files"""
    run_check_format_hdl()
    run_check_format_python()


def run_check_format_hdl():
    """Check formatting in HDL files"""

    print("\nChecking HDL formatting...\n", flush=FLUSH)

    hdl_files = find_project_hdl_files()

    # Make a copy of original HDL code
    hdl_file_code_original = []
    for hdl_file in hdl_files:
        with open(hdl_file, "r") as f:
            hdl_file_code_original.append(f.readlines())

    # Run hdl formatter
    run_fix_format_hdl(print_output=False)

    # Make a copy of the formatted HDL code
    hdl_file_code_formatted = []
    for hdl_file in hdl_files:
        with open(hdl_file, "r") as f:
            hdl_file_code_formatted.append(f.readlines())

    colorama.init()
    is_diff = False
    for i in range(len(hdl_file_code_original)):
        original = hdl_file_code_original[i]
        formatted = hdl_file_code_formatted[i]
        fname = str(hdl_files[i])
        diff = list(
            unified_diff(original, formatted, fromfile=fname, tofile=fname, n=5)
        )
        if diff:
            is_diff = True
            print_unified_diff_in_color(diff)
    colorama.deinit()

    # Restore original HDL code
    for i in range(len(hdl_files)):
        with open(hdl_files[i], "w") as f:
            f.write("".join(hdl_file_code_original[i]))

    if is_diff:
        raise RuntimeError("HDL format check failed")


def print_unified_diff_in_color(diff):
    for line in diff:
        if line.startswith("---") or line.startswith("+++"):
            line = f"{Style.BRIGHT}{line}{Style.RESET_ALL}"
        elif line.startswith("@@"):
            line = f"{Fore.CYAN}{line}{Style.RESET_ALL}"
        elif line.startswith("-"):
            line = f"{Fore.RED}{line}{Style.RESET_ALL}"
        elif line.startswith("+"):
            line = f"{Fore.GREEN}{line}{Style.RESET_ALL}"
        print(line, end="", flush=FLUSH)
    print()


def run_check_format_python():
    """Check formatting in Python files"""
    print("\nChecking Python formatting...\n", flush=FLUSH)
    cmd = ["black", "--diff", "--check", "--color", "."]
    run(cmd)


def run_fix_format():
    """Fix formatting in all files"""
    print("\nFixing HDL formatting...\n", flush=FLUSH)
    run_fix_format_hdl()
    run_fix_format_python()


def run_fix_format_hdl(print_output=True):
    """Fix formatting in HDL files"""

    # Use --inplace flag to overwrite existing files
    cmd = ["verible-verilog-format", "--inplace"]

    # Add options from .verible-verilog-format.yaml if specified
    verible_verilog_format_yaml = PROJECT_ROOT / ".verible-verilog-format.yaml"
    yaml_data = None
    if verible_verilog_format_yaml.exists():
        with open(verible_verilog_format_yaml, "r") as f:
            yaml_data = yaml.safe_load(f.read())

    format_args = []
    for k, v in yaml_data.items():
        format_args.append(f"--{k}={v}")

    cmd += format_args

    hdl_files = find_project_hdl_files()
    cmd += [str(f) for f in hdl_files]

    run(cmd, print_output=print_output)


def run_fix_format_python():
    """Fix formatting in Python files"""

    print("\nFixing Python formatting...\n", flush=FLUSH)
    cmd = ["black", "."]
    run(cmd)


def run_lint():
    pass


def run_docs():
    """Make documentation"""

    DOCS_BUILD_DIR = DOCS_DIR / "build"

    # Delete entire docs build directory if it exists
    if DOCS_BUILD_DIR.exists():
        shutil.rmtree(DOCS_BUILD_DIR)

    # Create new docs build directory
    DOCS_BUILD_DIR.mkdir()

    # Generature SVG block diagram graphics
    run_generate_hdl_svgs()

    cmd = ["make", "html"]
    run(cmd, cwd=DOCS_DIR)


def run_generate_hdl_svgs():
    svg_path = DOCS_DIR / "source" / "svg"
    json_path = DOCS_DIR / "source" / "json"

    # Clear everything out of svg directory
    if svg_path.exists():
        shutil.rmtree(svg_path)
    svg_path.mkdir()

    # Create temporary json directory if it doesn't already exist
    if not json_path.exists():
        json_path.mkdir()

    # Add all SystemVerilog files in the src directory
    hdl_search_patterns = ["**/*.sv"]
    hdl_files = []
    for sp in hdl_search_patterns:
        hdl_files += SRC_DIR.glob(sp)

    print(hdl_files)

    # Ignore certain hdl files that fails svg generation despite
    # being synthesizable
    ignore_hdl_files = ["onehot_mux.sv"]
    hdl_files = [f for f in hdl_files if f.name not in ignore_hdl_files]

    print(hdl_files)

    svg_files = []
    json_files = []
    for f in hdl_files:
        svg_files += [svg_path / (f.stem + ".svg")]
        json_files += [json_path / (f.stem + ".json")]

    # Run yosys to output jsons and then use netlistsvg to create svgs for each module
    for i in range(len(hdl_files)):
        cmd = [
            "yosys",
            "-p",
            f"read -sv {hdl_files[i]}; proc; clean; json -o {json_files[i]}",
        ]
        run(cmd, cwd=DOCS_DIR)
        cmd = ["netlistsvg", f"{json_files[i]}", "-o", f"{svg_files[i]}"]
        run(cmd, cwd=DOCS_DIR)

    # Remove temporary json directory
    shutil.rmtree(json_path)


@click.command()
@click.option("--test", is_flag=True, help="Run tests")
@click.option("--check-format", is_flag=True, help="Check formatting")
@click.option("--fix-format", is_flag=True, help="Fix formatting")
@click.option("--lint", is_flag=True, help="Run linting")
@click.option("--docs", is_flag=True, help="Build documentation")
def precommit(test, check_format, fix_format, lint, docs):

    # if no flags are provided, then run default configuration
    if not any([test, check_format, fix_format, lint, docs]):
        test = True
        check_format = True
        fix_format = False
        lint = True
        docs = True

    # Check if in docker container
    if not in_docker():
        raise OSError(
            "Not in a docker container. This script must be run from within a docker"
            " container. See README.md for instructions."
        )
    else:

        # Resolve project root directory before proceeding
        if not PROJECT_ROOT.is_dir():
            raise FileNotFoundError(
                f"Cannot find project root directory: {PROJECT_ROOT}"
            )

        if test:
            print("\nRunning tests...\n", flush=FLUSH)
            run_test()

        if check_format:
            print("\nChecking formatting...\n", flush=FLUSH)
            run_check_format()

        if fix_format:
            print("\nFixing formatting...\n", flush=FLUSH)
            run_fix_format()

        if lint:
            print("\nLinting...\n", flush=FLUSH)
            run_lint()

        if docs:
            print("\nBuilding documentation...\n", flush=FLUSH)
            run_docs()


if __name__ == "__main__":
    precommit()
