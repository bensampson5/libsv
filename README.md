# OpenHDL
HDL IP library

## Build

`docker build --pull -f Dockerfile.dev --build-arg UID=$(id -u) --build-arg GID=$(id -g) -t openhdl .`

`docker run --rm -it -v $(pwd):/code openhdl`

```bash
mkdir build
cd build
cmake -G Ninja ..
ninja
```

## Run tests

`./tests/test_counter`


