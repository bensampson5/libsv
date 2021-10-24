[CI]: https://github.com/bensampson5/libsv/actions
[COCOTB]: https://github.com/cocotb/cocotb
[DOCKER]: https://www.docker.com/
[DOCKER_HUB]: https://hub.docker.com/
[DOCS]: https://libsv.readthedocs.io/en/latest/
[GTKWAVE]: http://gtkwave.sourceforge.net/
[LIBSV_DOCKER_HUB]: https://hub.docker.com/repository/docker/bensampson5/libsv
[PYTEST]: [https://github.com/pytest-dev/pytest]
[SPHINX]: https://www.sphinx-doc.org/en/master/
[VERIBLE]: https://github.com/google/verible
[VERILATOR]: https://github.com/verilator/verilator

# LibSV
Welcome to LibSV! [Click here to go to LibSV's documentation][DOCS].

## About

LibSV is a library of open source, parameterized digital logic IP written in SystemVerilog. While other similar libraries
 do exist, LibSV is unique in that it takes advantage of open-source, state-of-the-art development best practices and tools
 from across the software and digital design community:
- Python-based, integrated with [pytest][PYTEST], automated testbenches using [Cocotb][COCOTB] + [Verilator][VERILATOR]
  for easy-to-use, fast logic simulation
- All testbenches output waveform files in FST format for viewing with [GTKWave][GTKWAVE]
- [Extensive documention][DOCS] using [Sphinx][SPHINX] that includes circuit schematics for each module
- Automated formatting and lint checks using [Verible][VERIBLE]
- [Continuous integration (CI) workflows][CI] integrated with [Docker][DOCKER]
- [LibSV docker images][LIBSV_DOCKER_HUB] published to [Docker Hub][DOCKER_HUB]


## Getting Started

The easiest way to get started with LibSV is with the publicly available [LibSV docker images on Docker Hub][LIBSV_DOCKER_HUB].
To use an LibSV docker image, first you'll need to install [Docker](https://www.docker.com/get-started), if you don't already have it.

## Running Tests

To run LibSV tests, first, pull the latest LibSV docker image:

```bash
docker build --pull -f Dockerfile.dev \
    --build-arg UID=$(id -u) \
    --build-arg GID=$(id -g) \
    -t libsv .
```

Then, start a new docker container using the LibSV image and mount the project root folder to the container:

```bash
docker run --rm -it -v $(pwd):/code libsv
```

Finally, within the Docker container, run `pytest` - That's it!
```bash
pytest
```

Each test generates an associated `.fst` waveform file that is written out to the `build/` directory that can be viewed
using [GTKWave][GTKWAVE].
