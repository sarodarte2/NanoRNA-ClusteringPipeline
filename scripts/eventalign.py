#!/usr/bin/env python3
"""
Align events using f5c.
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
    parser = ArgumentParser(description="Align events using f5c.")
    parser.add_argument('--config', required=True, type=str, help="Path to pipeline configuration file")
    parser.add_argument('--output', required=True, type=str, help="Path to output directory for event alignments")
    return parser.parse_args()

def event_align_reads(fastq, sorted_bam, reference, output, threads, f5c_path, fast5):
    """
    Align events using f5c.
    """
    os.makedirs(output, exist_ok=True)
    output_file = os.path.join(output, "events.tsv")
    command = f"{f5c_path} eventalign -b {sorted_bam} -g {reference} -r {fastq} -d {fast5} --rna -t {threads} > {output_file}"

    logging.info(f"Executing command: {command}")
    try:
        check_call(command, shell=True)
        logging.info(f"Event alignment completed. Results saved to: {output_file}")
    except CalledProcessError as e:
        logging.error(f"f5c eventalign failed with exit status {e.returncode}")
        logging.error(f"Command: {e.cmd}")
        logging.error(f"Output: {e.output}")

def main():
    """
    Main function to execute the event alignment.
    """
    args = parse_args()
    config_file = args.config
    output = args.output
    cfg = config.load_config(config_file)

    logging.info("Starting event alignment.")
    event_align_reads(cfg['fastq'], cfg['sorted_bam'], cfg['reference'], Path(output), cfg['threads'], cfg['f5c_path'], cfg['fast5'])
    logging.info("Event alignment completed.")

if __name__ == "__main__":
    main()
