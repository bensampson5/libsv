[DOCS]: https://openhdl.readthedocs.io/en/latest/
[CI]: https://github.com/bensampson5/openhdl/actions
[VERIBLE]: https://github.com/google/verible
[VERILATOR]: https://github.com/verilator/verilator
[CATCH2]: https://github.com/catchorg/Catch2
[DOCKER]: https://www.docker.com/
[DOCKER_HUB]: https://hub.docker.com/
[OPENHDL_DOCKER_HUB]: https://hub.docker.com/repository/docker/bensampson5/openhdl
[SPHINX]: https://www.sphinx-doc.org/en/master/
[VCD]: https://en.wikipedia.org/wiki/Value_change_dump
[GTKWAVE]: http://gtkwave.sourceforge.net/
# OpenHDL
Welcome to OpenHDL! [Click here to go to OpenHDL's documentation][DOCS].

## About

OpenHDL is a library of open source, parameterized digital hardware designs. While other similar libraries do exist,
OpenHDL is unique in that it takes advantage of state-of-the-art development best practices and tools from the software community including:
- [Continuous integration (CI) workflows][CI] integrated with [Docker][DOCKER]
- [OpenHDL docker images][OPENHDL_DOCKER_HUB] published to [Docker Hub][DOCKER_HUB]
- Fast, automated unit testing using [Verilator][VERILATOR] and [Catch2][CATCH2] with [VCD][VCD] outputs for waveform viewing
- Automated formatting used [Verible][VERIBLE]
- [Extensive documention][DOCS] using [Sphinx][SPHINX]
- Useful examples that are easily built and run so you can get started with OpenHDL in minutes

## Getting Started

The easiest way to get started with OpenHDL is with the publicly available [OpenHDL docker images on Docker Hub][OPENHDL_DOCKER_HUB]. To use an OpenHDL docker image, first you'll need to install [Docker](https://www.docker.com/get-started), if you don't already have it.

### Building

OpenHDL only needs to be built if you want to run the unit tests or examples. To do this, first, pull the latest OpenHDL docker image:

```bash
docker build --pull -f Dockerfile.dev \
    --build-arg UID=$(id -u) \
    --build-arg GID=$(id -g) \
    -t openhdl .
```

Then, start a new docker container using the OpenHDL image and mount the project root folder to the container:

```bash
docker run --rm -it -v $(pwd):/code openhdl
```

Inside the container, create a `build` directory and configure `cmake` using the Ninja generator:

```bash
mkdir build
cd build
cmake -GNinja ..
```

Finally, build the OpenHDL unit tests and examples:
```bash
ninja
```

### Running Unit Tests

After building, unit test executables are available for running all or specific unit tests.

All unit tests can be run using the `ctest` command which is linked to the Catch2 unit testing framework. All tests can be run in the build directory using:

```bash
ctest
```

To list all available tests, run:

```bash
ctest -N
```

To run a specific test, use the `-R` flag:
```bash
ctest -R "Scenario: Counter can reset"
```

To run all unit tests for a specific design, run the test executable for that design. For example, for [counter.sv](https://github.com/bensampson5/openhdl/blob/main/src/base/counter/counter.sv) this would be:

```bash
cd ./test/base/counter
./test_counter
```

Most designs in OpenHDL have more then one unit test scenario, to see all the unit test scenarios for a specific design, use the `-l` flag:

```bash
./test_counter -l
```

Then a specific unit test scenario for a specific OpenHDL design can be run using the module-specific executable with:

```bash
./test_counter "Scenario: Counter can be reset"
```

### Viewing the Simulation Waveform Output

For each unit test scenario, an associated .vcd waveform file that matches the scenario name is generated when it is run.

These VCD files can be viewed with a waveform viewer of your choice. For example, [GTKWave][GTKWAVE].