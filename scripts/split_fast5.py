#!/usr/bin/env python3
"""
Split multi-read FAST5 files into single-read FAST5 files.
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
    parser = ArgumentParser(description="Split multi-read FAST5 files into single-read FAST5 files.")
    parser.add_argument('--config', required=True, type=str, help="Path to pipeline configuration file")
    parser.add_argument('--output', required=True, type=str, help="Path to output directory for split FAST5 files")
    return parser.parse_args()

def split_fast5_files(fast5, output, threads, multi_to_single_fast5_path):
    """
    Split multi-read FAST5 files into single-read FAST5 files.
    """
    check_call(f"{multi_to_single_fast5_path} --threads {threads} --input_path {fast5} --save_path {output}".split())
    logging.info(f"FAST5 files split and saved to: {output}")

def main():
    """
    Main function to execute the split_fast5_files function.
    """
    args = parse_args()
    config_file = args.config
    output = args.output
    cfg = config.load_config(config_file)

    split_fast5_files(cfg['fast5'], Path(output), cfg['threads'], cfg['multi_to_single_fast5_path'])

if __name__ == "__main__":
    main()
