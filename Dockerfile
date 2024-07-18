# Use a base image with the necessary dependencies
FROM ubuntu:20.04

# Install dependencies
RUN apt-get update && \
    apt-get install -y build-essential wget git python3 python3-venv python3-pip gcc g++-9 make zlib1g-dev libbz2-dev liblzma-dev libcurl4-gnutls-dev samtools minimap2

# Install VBZ compression plugin
RUN wget https://github.com/nanoporetech/vbz_compression/releases/download/1.0.2/ont-vbz-hdf-plugin_1.0.2-1.bionic_amd64.deb && \
    dpkg -i ont-vbz-hdf-plugin_1.0.2-1.bionic_amd64.deb && \
    rm ont-vbz-hdf-plugin_1.0.2-1.bionic_amd64.deb

# Set HDF5 plugin path
ENV HDF5_PLUGIN_PATH=/usr/local/hdf5/lib/plugin

# Set up Python environment
RUN python3 -m venv /env
ENV PATH="/env/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the pipeline code
COPY . /root/NanoRNA-ClusteringPipeline
WORKDIR /root/NanoRNA-ClusteringPipeline

# Install ont-fast5-api and pycoqc
RUN pip install ont-fast5-api pycoqc

# Install Nanopolish
RUN git clone --recursive https://github.com/jts/nanopolish.git tools/nanopolish && \
    cd tools/nanopolish && \
    make && \
    cd ../..

# Install GeLuster
RUN git clone https://github.com/yutingsdu/GeLuster.git tools/GeLuster && \
    cd tools/GeLuster/src && \
    make release && \
    cd ../..

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
