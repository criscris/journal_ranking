FROM ubuntu:bionic

WORKDIR /root

RUN apt update && \
  apt install -y \
    curl \
    wget \
    git \
    python3-pip \
    python3-dev \
    docker.io

RUN pip3 install --upgrade pip && \
  pip3 install -U \
    numpy==1.18.2 \
    pandas==1.0.5 \
    pylint==2.5.2

CMD /bin/bash
