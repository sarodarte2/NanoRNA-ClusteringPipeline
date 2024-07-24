#!/usr/bin/env python3
"""
Run the entire RNA sequencing analysis pipeline.
"""

import os
from subprocess import check_call
from argparse import ArgumentParser
from pathlib import Path
import config
import logging
from datetime import datetime
import multiprocessing

def parse_args():
    """
    Parse command-line arguments.
    """
    parser = ArgumentParser(description="Run the entire RNA sequencing analysis pipeline.")
    parser.add_argument('--config', required=True, type=str, help="Path to pipeline configuration file")
    return parser.parse_args()

def setup_output_directories(base_output):
    """
    Create dated output directory with subdirectories.
    """
    date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = Path(base_output) / f"{date_str}_output"
    subdirs = {
        'split_fast5_output': output_dir / 'fast5s',
        'index_output': output_dir / 'index',
        'alignment_output': output_dir / 'alignment',
        'cluster_output': output_dir / 'cluster',
        'polya_output': output_dir / 'polya',
        'pycoqc_output': output_dir / 'pycoqc',
        'eventalign_output': output_dir / 'eventalign',
        'log_output': output_dir / 'logs'
    }
    for subdir in subdirs.values():
        subdir.mkdir(parents=True, exist_ok=True)
    
    return output_dir, subdirs

def setup_logging(log_output):
    """
    Set up logging configuration.
    """
    log_file = log_output / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return log_file

def get_max_threads():
    """
    Get the maximum number of available threads.
    """
    return multiprocessing.cpu_count()

def main():
    """
    Main function to execute the pipeline steps.
    """
    args = parse_args()
    config_file = args.config
    cfg = config.load_config(config_file)

    base_output = cfg['output']
    output_dir, subdirs = setup_output_directories(base_output)
    log_file = setup_logging(subdirs['log_output'])
    
    # Dynamically set the maximum number of threads
    max_threads = get_max_threads()
    cfg['threads'] = max_threads
    config.save_config(config_file, cfg)

    logging.info(f"Pipeline started with {max_threads} threads. Output directory: {output_dir}")

    # Step 1: Split FAST5 files
    split_fast5_script = Path(__file__).parent / "split_fast5.py"
    check_call(f"python3 {split_fast5_script} --config {config_file} --output {subdirs['split_fast5_output']}".split())
    logging.info("Step 1: Split FAST5 files completed successfully.")

    # Step 2: Index reads
    index_reads_script = Path(__file__).parent / "index_reads.py"
    check_call(f"python3 {index_reads_script} --config {config_file} --output {subdirs['index_output']}".split())
    logging.info("Step 2: Index reads completed successfully.")

    # Step 3: Align and filter FASTQ reads
    align_script = Path(__file__).parent / "align.py"
    check_call(f"python3 {align_script} --config {config_file} --output {subdirs['alignment_output']}".split())
    logging.info("Step 3: Align and filter FASTQ reads completed successfully.")

    # Step 4: Generate PycoQC report
    pycoqc_script = Path(__file__).parent / "pycoqc_report.py"
    check_call(f"python3 {pycoqc_script} --config {config_file} --output {subdirs['pycoqc_output']}".split())
    logging.info("Step 4: Generate PycoQC report completed successfully.")

    # Step 5: Cluster reads
    cluster_script = Path(__file__).parent / "cluster_reads.py"
    check_call(f"python3 {cluster_script} --config {config_file} --output {subdirs['cluster_output']}".split())
    logging.info("Step 5: Cluster reads completed successfully.")

    # Step 6: Poly-A tail estimation
    polya_script = Path(__file__).parent / "estimate_polya.py"
    check_call(f"python3 {polya_script} --config {config_file} --output {subdirs['polya_output']}".split())
    logging.info("Step 6: Poly-A tail estimation completed successfully.")
    
    # Step 7: Event alignment
    eventalign_script = Path(__file__).parent / "eventalign.py"
    check_call(f"python3 {eventalign_script} --config {config_file} --output {subdirs['eventalign_output']}".split())
    logging.info("Step 7: Event alignment completed successfully.")

    logging.info("Pipeline completed successfully.")
    print(f"Pipeline completed successfully. Log file: {log_file}")

if __name__ == "__main__":
    main()
