#!/bin/bash

# Check if the script is run from the repository directory
if [ ! -f "requirements.txt" ]; then
  echo "Please run this script from the root directory of the cloned repository."
  exit 1
fi

# Set up directories
mkdir -p ~/local/hdf5/lib/plugin
mkdir -p tools

# Update and install system dependencies
sudo apt-get update
sudo apt-get install -y build-essential wget git python3 python3-venv python3-pip samtools

# Download and install VBZ compression plugin
wget https://github.com/nanoporetech/vbz_compression/releases/download/1.0.2/ont-vbz-hdf-plugin_1.0.2-1.bionic_amd64.deb -O ~/local/ont-vbz-hdf-plugin_1.0.2-1.bionic_amd64.deb
sudo dpkg -i ~/local/ont-vbz-hdf-plugin_1.0.2-1.bionic_amd64.deb

# Set up HDF5 plugin path
export HDF5_PLUGIN_PATH=/usr/local/hdf5/lib/plugin
echo 'export HDF5_PLUGIN_PATH=/usr/local/hdf5/lib/plugin' >> ~/.bashrc

# Set up Python virtual environment
python3 -m venv env
source env/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install additional tools
# ont-fast5-api
pip install ont-fast5-api pycoqc

# Nanopolish
git clone --recursive https://github.com/jts/nanopolish.git tools/nanopolish
cd tools/nanopolish
make
cd ../..

# minimap2
git clone https://github.com/lh3/minimap2 tools/minimap2
cd tools/minimap2
make
cd ../..

# GeLuster
git clone https://github.com/yutingsdu/GeLuster.git tools/GeLuster
cd tools/GeLuster/src
make release
cd ../../..

# Get the absolute paths for the tools
NANOPOLISH_PATH=$(pwd)/tools/nanopolish/nanopolish
MINIMAP2_PATH=$(pwd)/tools/minimap2/minimap2
GELUSTER_PATH=$(pwd)/tools/GeLuster/GeLuster
PYCOQC_PATH=$(which pycoQC)
MULTI_TO_SINGLE_FAST5_PATH=$(which multi_to_single_fast5)

# Update the configuration file with the correct paths
CONFIG_FILE="config/pipeline_config.yaml"
sed -i "s|nanopolish_path:.*|nanopolish_path: $NANOPOLISH_PATH|" $CONFIG_FILE
sed -i "s|aligner_path:.*|aligner_path: $MINIMAP2_PATH|" $CONFIG_FILE
sed -i "s|geluster_path:.*|geluster_path: $GELUSTER_PATH|" $CONFIG_FILE
sed -i "s|pycoqc_path:.*|pycoqc_path: $PYCOQC_PATH|" $CONFIG_FILE
sed -i "s|multi_to_single_fast5_path:.*|multi_to_single_fast5_path: $MULTI_TO_SINGLE_FAST5_PATH|" $CONFIG_FILE

# Export paths to ~/.bashrc for future sessions
echo 'export PATH=$PATH:'$(pwd)'/tools/nanopolish' >> ~/.bashrc
echo 'export PATH=$PATH:'$(pwd)'/tools/minimap2' >> ~/.bashrc
echo 'export PATH=$PATH:'$(pwd)'/tools/GeLuster' >> ~/.bashrc
echo 'export HDF5_PLUGIN_PATH=/usr/local/hdf5/lib/plugin' >> ~/.bashrc

# Source ~/.bashrc to apply changes
source ~/.bashrc

echo "Setup completed successfully."