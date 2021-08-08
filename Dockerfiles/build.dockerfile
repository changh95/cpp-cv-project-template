FROM ubuntu:latest

MAINTAINER changh95

ARG DEBIAN_FRONTEND=noninteractive
ARG BRANCH=Development

RUN apt-get -y update &&\
apt-get -y install sudo git wget curl cmake build-essential &&\
apt-get -y install python3 python3-pip &&\
pip3 install pyaml &&\
apt-get autoclean

RUN mkdir cpp-cv-project-template &&\
cd cpp-cv-project-template &&\
git clone https://github.com/changh95/cpp-cv-project-template.git . &&\
git remote update &&\
git fetch --all &&\
git checkout ${BRANCH}} &&\
git pull &&\
git branch &&\
./setup.py

