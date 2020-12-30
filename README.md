# OpenHDL {#mainpage}
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


