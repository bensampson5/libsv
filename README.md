# OpenHDL
HDL IP library

## Build

`docker build -f Dockerfile.dev --build-arg UID=$(id -u) --build-arg GID=$(id -g) -t openhdl .`

`docker run --rm -it -v $(pwd):/code openhdl`

```bash
mkdir build
cd build
cmake ..
make -j$(nproc)
```

## Run tests

`./tests/Vcounter`


