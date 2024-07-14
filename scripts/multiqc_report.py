#!/usr/bin/env python3
"""
Generate MultiQC report.
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
    parser = ArgumentParser(description="Generate MultiQC report.")
    parser.add_argument('--config', required=True, type=str, help="Path to pipeline configuration file")
    parser.add_argument('--output', required=True, type=str, help="Path to output directory for MultiQC report")
    return parser.parse_args()

def generate_multiqc_report(fast5, output):
    """
    Generate MultiQC report from FAST5 files.

    Parameters:
    fast5 (str): Path to the directory containing single-read FAST5 files.
    output (str): Path to the output directory where the MultiQC report will be saved.
    """
    check_call(f"multiqc {fast5} -o {output}".split())
    logging.info(f"MultiQC report generated and saved to: {output}")

def main():
    """
    Main function to execute the generate_multiqc_report function.
    """
    args = parse_args()
    config_file = args.config
    output = args.output
    cfg = config.load_config(config_file)

    generate_multiqc_report(cfg['fast5'], Path(output))

if __name__ == "__main__":
    main()
