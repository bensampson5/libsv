from pathlib import Path
import subprocess
import shutil

def run(cmd, cwd=".", check_exit=True):
    p = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )

    while True:
        stdout = p.stdout.readline()
        if stdout == "" and p.poll() is not None:
            break
        if stdout:
            print(stdout, end="", flush=True)

    if check_exit and p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, " ".join(cmd))

def gen_hdl_svg():
    cwd = Path.cwd()
    src_path = Path("../../src").resolve()
    svg_path = cwd / "svg"
    json_path = cwd / "json"

    if not svg_path.exists():
        svg_path.mkdir()

    if not json_path.exists():
        json_path.mkdir()

    # Add all SystemVerilog or Verilog files in the src directory
    hdl_search_patterns = ["**/*.sv", "**/*.v"]
    hdl_files = []
    for sp in hdl_search_patterns:
        hdl_files += src_path.glob(sp)

    svg_files = []
    json_files = []
    for f in hdl_files:
        svg_files += [svg_path / (f.stem + ".svg")]
        json_files += [json_path / (f.stem + ".json")]

    for i in range(len(hdl_files)):
        cmd = ["yosys", "-p", f"read -sv {hdl_files[i]}; proc; opt; clean; json -o {json_files[i]}"]
        run(cmd)
        cmd = ["netlistsvg", f"{json_files[i]}", "-o", f"{svg_files[i]}"]
        run(cmd)

    # Remove jsons
    shutil.rmtree(json_path)
