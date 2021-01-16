FROM ubuntu:20.04

WORKDIR /tmp

# Baseline apt-get installs
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
                        autoconf \
                        bc \
                        bison \
                        build-essential \
                        ca-certificates \
                        ccache \
                        clang-format \
                        cmake \
                        curl \
                        flex \
                        git \
                        gnupg \
                        libfl-dev \
                        libgoogle-perftools-dev \
                        ninja-build \
                        perl \
                        python3 \
                        python3-pip \
                        wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add Bazel distribution URI as a package source
RUN curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor > bazel.gpg \
    && mv bazel.gpg /etc/apt/trusted.gpg.d/ \
    && echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list

# Install Bazel
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
                        bazel \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install python packages using pip
RUN pip3 install cmake-format sphinx sphinx-rtd-theme sphinxcontrib-hdl-diagrams

# Link python3 to system python
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip

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

# Install Verible
ARG VERIBLE_URL=https://github.com/google/verible/releases/download/v0.0-879-g181c8f3/verible-v0.0-879-g181c8f3-Ubuntu-20.04-focal-x86_64.tar.gz
RUN wget ${VERIBLE_URL} -O verible.tar.gz \
    && mkdir verible \
    && tar -xf verible.tar.gz -C verible --strip-components=1 \
    && cp -r verible/bin/* /usr/local/bin \
    && rm -rf verible verible.tar.gz


WORKDIR /root
CMD /bin/bash