#!/usr/bin/env python3
"""
Generate PycoQC report from sequencing summary file.
"""

import os
from subprocess import check_call, CalledProcessError, Popen, PIPE
from argparse import ArgumentParser
from pathlib import Path
import config
import logging
import gzip
import shutil

def parse_args():
    """
    Parse command-line arguments.
    """
    parser = ArgumentParser(description="Generate PycoQC report from sequencing summary file.")
    parser.add_argument('--config', required=True, type=str, help="Path to pipeline configuration file")
    parser.add_argument('--output', required=True, type=str, help="Output directory")
    return parser.parse_args()

def gzip_file(file_path):
    """
    Gzip the given file.
    """
    with open(file_path, 'rb') as f_in:
        with gzip.open(file_path + '.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return file_path + '.gz'

def generate_pycoqc_report(summary_file, output_dir, pycoqc_path):
    """
    Generate PycoQC report from sequencing summary file.
    
    Parameters:
    summary_file (str): Path to the sequencing summary file.
    output_dir (str): Path to the output directory where the PycoQC report will be saved.
    pycoqc_path (str): Path to the PycoQC executable.
    """
    gzipped_summary_file = gzip_file(summary_file)
    output_file = Path(output_dir) / 'pycoqc_report.html'
    command = f"{pycoqc_path} -f {gzipped_summary_file} -o {output_file}".split()
    process = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        logging.error(f"PycoQC failed with exit status {process.returncode}")
        logging.error(f"Command: {' '.join(command)}")
        logging.error(f"Stdout: {stdout.decode()}")
        logging.error(f"Stderr: {stderr.decode()}")
        raise CalledProcessError(process.returncode, command)
    
    logging.info(f"PycoQC report generated and saved to: {output_file}")

def main():
    """
    Main function to run the PycoQC report generation.
    """
    args = parse_args()
    config_file = args.config
    output = args.output
    cfg = config.load_config(config_file)

    logging.info("Starting PycoQC report generation.")
    generate_pycoqc_report(cfg['sequencing_summary'], Path(output), cfg['pycoqc_path'])
    logging.info("PycoQC report generation completed.")

if __name__ == "__main__":
    main()
