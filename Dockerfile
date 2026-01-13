FROM ubuntu:22.04

# ARG CUDA_ARCHITECTURES=native

# Prevent stop building ubuntu at time zone selection.
ENV DEBIAN_FRONTEND=noninteractive

# Prepare an empty machine for building.
RUN apt-get update && \
    apt-get install -y \
        sudo \
        git \
        ccache \
        cmake \
        unzip \
        ninja-build \
        build-essential \
        gfortran \
        ripgrep \
        fd-find \
        python3 \
        python3-pip \
        intel-mkl \
        libatlas-base-dev \
        liblapack-dev \
        libblas-dev

# Install python dependencies for build_dependencies.py
RUN pip3 install --upgrade pip
RUN pip3 install gitpython pyyaml

## For AMD CPUs using intel-mkl
ENV MKL_DEBUG_CPU_TYPE=5

## Copy repo to container, then build dependencies
COPY . /cpp-cv-project/
WORKDIR /cpp-cv-project/
RUN chmod +x build_dependencies.py && \
    ./build_dependencies.py --d

# Build the main project, check if dependencies are correctly installed
RUN cmake -S . -B ./build -DCMAKE_BUILD_TYPE=Debug
RUN cmake --build ./build
RUN ./build/bin/solution

# Provide folders for mounting data and documents
WORKDIR /
RUN mkdir -p /Documents/ /data/
CMD ["/bin/bash"]
