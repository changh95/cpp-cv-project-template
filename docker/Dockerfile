FROM ubuntu:jammy

# ARG CUDA_ARCHITECTURES=native

# Prevent stop building ubuntu at time zone selection.
ENV DEBIAN_FRONTEND=noninteractive

# Prepare and empty machine for building.
RUN apt-get update
RUN apt-get install -y \
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
    git checkout feat/big_change && \
    python3 ./build_dependencies.py --d
#RUN git clone https://github.com/colmap/colmap.git
#RUN cd colmap && \
#    git reset --hard ${COLMAP_VERSION} && \
#    mkdir build && \
#    cd build && \
#    cmake .. -GNinja -DCMAKE_CUDA_ARCHITECTURES=${CUDA_ARCHITECTURES} && \
#    ninja && \
#    ninja install && \
#    cd .. && rm -rf colmap
