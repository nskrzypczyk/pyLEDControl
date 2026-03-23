FROM mcr.microsoft.com/devcontainers/base:ubuntu

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        git curl \
        python3-dev \
        build-essential \
        libjpeg-dev \
        nodejs npm gcc make cython3 \
        libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev libffi-dev liblzma-dev \
        libopenjp2-7 libtiff5-dev libsdl2-dev libtinfo-dev libopenblas-dev \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /workspaces/pyLEDControl
COPY . .