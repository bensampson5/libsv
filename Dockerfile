FROM ubuntu:20.04

WORKDIR /tmp

# Baseline apt-get installs
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        autoconf \
        bc \
        bison \
        ca-certificates \
        ccache \
        curl \
        flex \
        g++ \
        git \
        gnupg \
        libfl2 \
        libfl-dev \
        libgoogle-perftools-dev \
        make \
        npm \
        numactl \
        perl \
        perl-doc \
        python3-dev \
        python3-pip \
        wget \
        yosys \
        zlibc \
        zlib1g \
        zlib1g-dev \
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

# Install python packages using pip from requirements.txt
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Build and install Verilator v4.106 from source
ARG REPO=https://github.com/verilator/verilator
ARG TAG=v4.106
RUN git clone --depth 1 --branch "${TAG}" "${REPO}" verilator \
    && cd verilator \
    && autoconf \
    && ./configure \
    && make -j$(nproc) \
    && make install \
    && cd .. \
    && rm -rf verilator

# Install Verible
ARG VERIBLE_URL=https://github.com/google/verible/releases/download/v0.0-879-g181c8f3/verible-v0.0-879-g181c8f3-Ubuntu-20.04-focal-x86_64.tar.gz
RUN wget ${VERIBLE_URL} -O verible.tar.gz \
    && mkdir verible \
    && tar -xf verible.tar.gz -C verible --strip-components=1 \
    && cp -r verible/bin/* /usr/local/bin \
    && rm -rf verible verible.tar.gz

# Install netlistsvg using npm
RUN npm install -g netlistsvg

WORKDIR /root
CMD /bin/bash