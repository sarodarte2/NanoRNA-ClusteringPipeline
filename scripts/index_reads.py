#!/usr/bin/env python3
"""
Index reads for Nanopolish.
"""

import os
from subprocess import check_call
from argparse import ArgumentParser
from pathlib import Path
import config
import logging

def parse_args():
    """
    Parse command-line arguments.
    """
    parser = ArgumentParser(description="Index reads for Nanopolish.")
    parser.add_argument('--config', required=True, type=str, help="Path to pipeline configuration file")
    parser.add_argument('--output', required=True, type=str, help="Path to output directory for index files")
    return parser.parse_args()

def index_reads(fast5, fastq, output, threads, nanopolish_path):
    """
    Index reads for Nanopolish.
    """
    readdb_path = output / 'nanopolish.readdb'
    check_call(f"{nanopolish_path} index -d {fast5} -s sequencing_summary.txt {fastq}".split())
    logging.info(f"Reads indexed and saved to: {readdb_path}")
    return readdb_path

def main():
    """
    Main function to execute the index_reads function.
    """
    args = parse_args()
    config_file = args.config
    output = args.output
    cfg = config.load_config(config_file)

    index_reads(cfg['fast5'], cfg['fastq'], Path(output), cfg['threads'], cfg['nanopolish_path'])

if __name__ == "__main__":
    main()
