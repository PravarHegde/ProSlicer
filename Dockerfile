FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential cmake git gettext libglib2.0-dev \
    libgtk-3-dev libarchive-dev libcurl4-openssl-dev \
    libgtest-dev libcgal-dev libglu1-mesa-dev libdbus-1-dev \
    libwebkit2gtk-4.0-dev libosmesa6-dev curl

WORKDIR /workspace
COPY . /workspace

# This Dockerfile allows compiling and running ProSlicer (Orca) headlessly in the cloud
# CMD ["./build_linux.sh"]
