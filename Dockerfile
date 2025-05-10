FROM ubuntu:18.04

ARG COPTER_TAG=Copter-4.5.7

RUN apt-get update && apt-get install -y \
    software-properties-common \
    wget \
    gnupg \
    sudo \
    lsb-release \
    git

RUN add-apt-repository ppa:ubuntu-toolchain-r/test -y && \
    apt-get update
RUN apt-get install -y gcc-10 g++-10

ENV CC=gcc-10
ENV CXX=g++-10

RUN git clone https://github.com/ArduPilot/ardupilot.git ardupilot
WORKDIR /ardupilot

RUN git checkout ${COPTER_TAG}

RUN git submodule update --init --recursive

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata

RUN useradd -m -s /bin/bash docker && \
    usermod -aG sudo docker && \ 
    echo "docker ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN chown -R docker:docker /ardupilot

USER docker
ENV USER=docker

RUN git config --global --add safe.directory /ardupilot
RUN find /ardupilot -name ".git" | sed 's/\/.git$//' | while read d; do \
    git config --global --add safe.directory "$d"; \
done

RUN Tools/environment_install/install-prereqs-ubuntu.sh -y

RUN ./waf distclean
RUN ./waf configure --board sitl
RUN ./waf copter
RUN ./waf rover 
RUN ./waf plane
RUN ./waf sub

EXPOSE 5760/tcp

ENV INSTANCE=0
ENV LAT=42.3898
ENV LON=-71.1476
ENV ALT=14
ENV DIR=270
ENV MODEL=+
ENV SPEEDUP=1
ENV VEHICLE=ArduCopter

ENTRYPOINT [ "sh", "-c", "/ardupilot/Tools/autotest/sim_vehicle.py --vehicle $VEHICLE -I$INSTANCE --custom-location=$LAT,$LON,$ALT,$DIR -w --frame $MODEL --no-rebuild --no-mavproxy --speedup $SPEEDUP" ]

