# OpenHDL
HDL IP library

## Build

```bash
docker build --pull -f Dockerfile.dev --build-arg UID=$(id -u) --build-arg GID=$(id -g) -t openhdl .
```

```bash
docker run --rm -it -v $(pwd):/code openhdl
```

```bash
mkdir build
cd build
cmake -G Ninja ..
ninja
```

## Run tests

```bash
./tests/test_main
```

Outputs vcd waveform files for all the test scenarios for the directory the above command is run in.

## View simulation waveform output for a test scenario

This should be done outside of the docker container using whatever waveform viewer that you want.

As an example for ``gtkwave`` this is:

```bash
gtkwave insert_vcd_file_name_here.vcd
```


