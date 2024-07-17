#!/usr/bin/env python3
"""
Index reads using Nanopolish and index BAM file using samtools.
"""

import os
from subprocess import check_call, CalledProcessError, Popen, PIPE
from argparse import ArgumentParser
from pathlib import Path
import config
import logging

def parse_args():
    """
    Parse command-line arguments.
    """
    parser = ArgumentParser(description="Index reads using Nanopolish and index BAM file using samtools.")
    parser.add_argument('--config', required=True, type=str, help="Path to pipeline configuration file")
    parser.add_argument('--output', required=True, type=str, help="Output directory")
    return parser.parse_args()

def index_reads(fast5, fastq, output, threads, nanopolish_path, sequencing_summary):
    """
    Index reads using Nanopolish.
    """
    os.makedirs(output, exist_ok=True)
    check_call(f"{nanopolish_path} index -d {fast5} -s {sequencing_summary} {fastq}".split())

def main():
    """
    Main function to run the indexing.
    """
    args = parse_args()
    config_file = args.config
    output = args.output
    cfg = config.load_config(config_file)

    logging.info("Starting read indexing.")
    index_reads(cfg['fast5'], cfg['fastq'], Path(output), cfg['threads'], cfg['nanopolish_path'], cfg['sequencing_summary'])
    logging.info("Read indexing completed.")

if __name__ == "__main__":
    main()

