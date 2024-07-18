#!/usr/bin/env python3
"""
Cluster reads.
"""

import os
from subprocess import check_call, CalledProcessError
from argparse import ArgumentParser
from pathlib import Path
import config
import logging

def parse_args():
    """
    Parse command-line arguments.
    """
    parser = ArgumentParser(description="Cluster reads.")
    parser.add_argument('--config', required=True, type=str, help="Path to pipeline configuration file")
    parser.add_argument('--output', required=True, type=str, help="Path to output directory for clustering results")
    parser.add_argument('--additional_samples', type=str, help="Paths to additional sample FASTQ files, separated by commas", default="")
    return parser.parse_args()

def cluster_reads(fastq, output, threads, additional_samples, geluster_path):
    """
    Cluster reads using GeLuster.

    Parameters:
    fastq (str): Path to the concatenated FASTQ file.
    output (str): Path to the output directory where clustering results will be saved.
    threads (int): Number of threads to use for the operation.
    additional_samples (str): Comma-separated list of paths to additional sample FASTQ files.
    """
    os.makedirs(output, exist_ok=True)

    additional_samples_flag = f"--multi {additional_samples}" if additional_samples else ""
    command = f"{geluster_path} -r {fastq} -i 6 -s dRNA -t {threads} -f fq -o {output} {additional_samples_flag}"

    logging.info(f"Executing command: {command}")
    print(f"Executing command: {command}")  # Print the command for debugging purposes
    try:
        check_call(command.split())
        logging.info(f"Reads clustered and saved to: {output}")
    except CalledProcessError as e:
        logging.error(f"GeLuster failed with exit status {e.returncode}")
        logging.error(f"Command: {e.cmd}")
        logging.error(f"Output: {e.output}")

def main():
    """
    Main function to execute the cluster_reads function.
    """
    args = parse_args()
    config_file = args.config
    output = args.output
    cfg = config.load_config(config_file)

    additional_samples = args.additional_samples
    cluster_reads(cfg['fastq'], Path(output), cfg['threads'], additional_samples, cfg['geluster_path'])

if __name__ == "__main__":
    main()

