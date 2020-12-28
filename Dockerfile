FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
                        autoconf \
                        bc \
                        bison \
                        build-essential \
                        ca-certificates \
                        ccache \
                        flex \
                        git \
                        libfl-dev \
                        libgoogle-perftools-dev \
                        perl \
                        python3 \
                        cmake \
                        gtkwave \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

# Build and install Verilator from source using git (use most recent 'stable' release)
ARG REPO=https://github.com/verilator/verilator
ARG TAG=stable
RUN git clone --depth 1 --branch "${TAG}" "${REPO}" verilator \
    && cd verilator \
    && autoconf \
    && ./configure \
    && make -j "$(nproc)" \
    && make install \
    && cd .. \
    && rm -rf verilator

# Install Catch2 (use v2.x branch)
ARG REPO=https://github.com/catchorg/Catch2
ARG TAG=v2.x
RUN git clone --depth 1 --branch "${TAG}" "${REPO}" Catch2 \
    && cd Catch2 \
    && cmake -Bbuild -H. -DBUILD_TESTING=OFF \
    && cmake --build build/ --target install \
    && cd .. \
    && rm -rf Catch2

WORKDIR /root
CMD /bin/bash