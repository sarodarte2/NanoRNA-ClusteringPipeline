#!/usr/bin/env python3
"""
Index reads using f5c and index BAM file using samtools.
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
    parser = ArgumentParser(description="Index reads using f5c and index BAM file using samtools.")
    parser.add_argument('--config', required=True, type=str, help="Path to pipeline configuration file")
    parser.add_argument('--output', required=True, type=str, help="Output directory")
    return parser.parse_args()

def index_reads(fast5, fastq, output, f5c_path, sequencing_summary):
    """
    Index reads using f5c.
    """
    os.makedirs(output, exist_ok=True)
    check_call(f"{f5c_path} index -d {fast5} -s {sequencing_summary} {fastq}".split())

def index_split_fast5_dirs(split_fast5_output, index_output, fastq, f5c_path, sequencing_summary):
    """
    Index each subdirectory of the split FAST5 output directory using f5c.
    """
    split_fast5_dirs = [d for d in Path(split_fast5_output).iterdir() if d.is_dir()]

    for fast5_dir in split_fast5_dirs:
        index_dir = Path(index_output) / fast5_dir.name
        os.makedirs(index_dir, exist_ok=True)
        try:
            command = f"{f5c_path} index -d {fast5_dir} -s {sequencing_summary} {fastq}"
            logging.info(f"Executing command: {command}")
            check_call(command.split())
            logging.info(f"Indexing completed for: {fast5_dir}")
        except CalledProcessError as e:
            logging.error(f"f5c index failed for {fast5_dir} with exit status {e.returncode}")
            logging.error(f"Command: {e.cmd}")
            logging.error(f"Output: {e.output}")

def main():
    """
    Main function to run the indexing.
    """
    args = parse_args()
    config_file = args.config
    output = args.output
    cfg = config.load_config(config_file)

    logging.info("Starting read indexing.")
    index_reads(cfg['fast5'], cfg['fastq'], Path(output), cfg['f5c_path'], cfg['sequencing_summary'])
    logging.info("Read indexing completed.")

    logging.info("Starting split FAST5 subdirectory indexing.")
    index_split_fast5_dirs(cfg['split_fast5_output'], cfg['index_output'], cfg['fastq'], cfg['f5c_path'], cfg['sequencing_summary'])
    logging.info("Split FAST5 subdirectory indexing completed.")

if __name__ == "__main__":
    main()
