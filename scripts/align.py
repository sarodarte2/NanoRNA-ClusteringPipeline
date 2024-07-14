#!/usr/bin/env python3
"""
Align and filter FASTQ reads.
"""

import os
from subprocess import check_call, Popen, PIPE
from argparse import ArgumentParser
from pathlib import Path
import config
import logging

def parse_args():
    """
    Parse command-line arguments.
    """
    parser = ArgumentParser(description="Align and filter FASTQ reads.")
    parser.add_argument('--config', required=True, type=str, help="Path to pipeline configuration file")
    parser.add_argument('--output', required=True, type=str, help="Path to output directory for alignment results")
    return parser.parse_args()

def align_and_filter_reads(fastq, reference, output, threads, aligner_path):
    """
    Align and filter FASTQ reads using minimap2 and samtools.
    """
    bam_path = os.path.join(output, os.path.basename(fastq).replace(".fastq", ".bam"))
    sorted_bam_path = bam_path.replace(".bam", ".sorted.bam")

    p1 = Popen(f"{aligner_path} -ax map-ont {reference} {fastq}".split(), stdout=PIPE)
    p2 = Popen(f"samtools sort -@ {threads} -o {sorted_bam_path}".split(), stdin=p1.stdout)
    p1.stdout.close()
    p2.communicate()

    check_call(f"samtools index {sorted_bam_path}".split())
    logging.info(f"Aligned and sorted BAM: {sorted_bam_path}")
    return sorted_bam_path

def main():
    """
    Main function to execute the align_and_filter_reads function.
    """
    args = parse_args()
    config_file = args.config
    output = args.output
    cfg = config.load_config(config_file)

    align_and_filter_reads(cfg['fastq'], cfg['reference'], Path(output), cfg['threads'], cfg['aligner_path'])

if __name__ == "__main__":
    main()
