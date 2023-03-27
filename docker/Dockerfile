FROM ubuntu:jammy

# ARG CUDA_ARCHITECTURES=native

# Prevent stop building ubuntu at time zone selection.
ARG BRANCH=develop
ENV DEBIAN_FRONTEND=noninteractive

# Prepare and empty machine for building.
RUN apt-get update
RUN apt-get install -y \
    sudo \
    git \
    cmake \
    ninja-build \
    build-essential \
    python3 \
    python3-pip
RUN pip3 install gitpython pyyaml

# Build and install
RUN git clone https://github.com/changh95/cpp-cv-project-template.git
RUN cd cpp-cv-project-template &&  \
    git remote update &&  \
    git remote prune origin &&  \
    git checkout ${BRANCH} && \
    ./build_dependencies.py --d
