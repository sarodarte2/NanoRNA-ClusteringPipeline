#!/bin/bash

# Activate the virtual environment
source env/bin/activate

# Source the ~/.bashrc to apply environment variables and paths
source ~/.bashrc

# Define the path to the configuration file
CONFIG_FILE="config/pipeline_config.yaml"

# Run the pipeline
python scripts/run_pipeline.py --config "$CONFIG_FILE"
