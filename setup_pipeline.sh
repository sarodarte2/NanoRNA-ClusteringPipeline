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
sudo apt-get install -y build-essential wget git python3 python3-venv python3-pip zlib1g-dev libbz2-dev liblzma-dev libcurl4-gnutls-dev libncurses5-dev samtools minimap2

# Verify and install CUDA if not already installed
if ! command -v nvcc &> /dev/null
then
    echo "CUDA not found. Installing CUDA..."
    # Verify CUDA-capable GPU
    lspci | grep -i nvidia || (sudo update-pciids && lspci | grep -i nvidia)
    
    # Install kernel headers
    sudo apt-get install linux-headers-$(uname -r)
    
    # Download and install CUDA toolkit
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-ubuntu2404.pin
    sudo mv cuda-ubuntu2404.pin /etc/apt/preferences.d/cuda-repository-pin-600
    wget https://developer.download.nvidia.com/compute/cuda/12.5.1/local_installers/cuda-repo-ubuntu2404-12-5-local_12.5.1-555.42.06-1_amd64.deb
    sudo dpkg -i cuda-repo-ubuntu2404-12-5-local_12.5.1-555.42.06-1_amd64.deb
    sudo cp /var/cuda-repo-ubuntu2404-12-5-local/cuda-*-keyring.gpg /usr/share/keyrings/
    sudo apt-get update
    sudo apt-get -y install cuda-toolkit-12-5
    
    # Install NVIDIA drivers
    sudo apt-get install -y nvidia-driver-555-open
    sudo apt-get install -y cuda-drivers-555
else
    echo "CUDA already installed."
fi

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
pip install ont-fast5-api pycoqc

# Download and extract f5c portable binaries
VERSION=v1.4
wget "https://github.com/hasindu2008/f5c/releases/download/$VERSION/f5c-$VERSION-binaries.tar.gz"
tar xvf f5c-$VERSION-binaries.tar.gz
mv f5c-$VERSION/* tools/f5c/
rm -rf f5c-$VERSION-binaries.tar.gz f5c-$VERSION

# Check if CUDA is installed and select the appropriate f5c binary
if command -v nvcc &> /dev/null
then
    F5C_PATH=$(pwd)/tools/f5c/f5c_x86_64_linux_cuda
else
    F5C_PATH=$(pwd)/tools/f5c/f5c_x86_64_linux
fi

# Nanopolish
if [ ! -d "tools/nanopolish" ]; then
  git clone --recursive https://github.com/jts/nanopolish.git tools/nanopolish
  cd tools/nanopolish
  make
  cd ../..
else
  echo "Nanopolish already installed."
fi

# GeLuster
if [ ! -d "tools/GeLuster" ]; then
  git clone https://github.com/yutingsdu/GeLuster.git tools/GeLuster
  cd tools/GeLuster/src
  make release
  cd ../..
else
  echo "GeLuster already installed."
fi

# Get the absolute paths for the tools
NANOPOLISH_PATH=$(pwd)/tools/nanopolish/nanopolish
MINIMAP2_PATH=$(which minimap2)
GELUSTER_PATH=$(pwd)/tools/GeLuster/GeLuster
SAMTOOLS_PATH=$(which samtools)
PYCOQC_PATH=$(which pycoQC)
MULTI_TO_SINGLE_FAST5_PATH=$(which multi_to_single_fast5)

# Get the absolute path to the configuration file
CONFIG_FILE=$(pwd)/config/pipeline_config.yaml

# Update the configuration file with the correct paths
sed -i "s|f5c_path:.*|f5c_path: $F5C_PATH|" $CONFIG_FILE
sed -i "s|nanopolish_path:.*|nanopolish_path: $NANOPOLISH_PATH|" $CONFIG_FILE
sed -i "s|aligner_path:.*|aligner_path: $MINIMAP2_PATH|" $CONFIG_FILE
sed -i "s|geluster_path:.*|geluster_path: $GELUSTER_PATH|" $CONFIG_FILE
sed -i "s|samtools_path:.*|samtools_path: $SAMTOOLS_PATH|" $CONFIG_FILE
sed -i "s|pycoqc_path:.*|pycoqc_path: $PYCOQC_PATH|" $CONFIG_FILE
sed -i "s|multi_to_single_fast5_path:.*|multi_to_single_fast5_path: $MULTI_TO_SINGLE_FAST5_PATH|" $CONFIG_FILE

# Export paths to ~/.bashrc for future sessions
echo 'export PATH=$PATH:'$(pwd)'/tools/f5c' >> ~/.bashrc
echo 'export PATH=$PATH:'$(pwd)'/tools/nanopolish' >> ~/.bashrc
echo 'export PATH=$PATH:'$(pwd)'/tools/GeLuster' >> ~/.bashrc
echo 'export HDF5_PLUGIN_PATH=/usr/local/hdf5/lib/plugin' >> ~/.bashrc

# Source ~/.bashrc to apply changes
source ~/.bashrc

echo "Setup completed successfully."
