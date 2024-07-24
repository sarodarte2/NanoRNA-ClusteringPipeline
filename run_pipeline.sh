#!/bin/bash

# Activate the virtual environment
source env/bin/activate

# Set HDF5_PLUGIN_PATH environment variable
export HDF5_PLUGIN_PATH=/usr/local/hdf5/lib/plugin

# Source the ~/.bashrc to apply environment variables and paths
source ~/.bashrc

# Define the path to the configuration file
CONFIG_FILE="config/pipeline_config.yaml"

# Run the pipeline
python3 scripts/run_pipeline.py --config "$CONFIG_FILE"
