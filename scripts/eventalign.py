#!/usr/bin/env python3
"""
Align events using Nanopolish eventalign.
"""

import os
import sys
import yaml
from pathlib import Path
from subprocess import check_call, CalledProcessError

def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

def eventalign(fastq, bam, reference, output, threads, nanopolish_path):
    output_file = output / "eventalign.tsv"
    with open(output_file, "w") as output_handle:
        try:
            check_call(
                f"{nanopolish_path} eventalign --reads {fastq} --bam {bam} --genome {reference} --threads {threads} --progress --scale-events".split(),
                stdout=output_handle
            )
            print(f"Event alignment completed. Results saved to {output_file}")
        except CalledProcessError as e:
            print(f"Nanopolish eventalign failed with exit status {e.returncode}")
            print(f"Command: {e.cmd}")
            raise

def main():
    config_file = sys.argv[2]
    output = Path(sys.argv[4])

    cfg = load_config(config_file)

    eventalign(cfg['fastq'], cfg['sorted_bam'], cfg['reference'], output, cfg['threads'], cfg['nanopolish_path'])

if __name__ == "__main__":
    main()
