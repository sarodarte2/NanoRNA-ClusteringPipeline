import os
from subprocess import check_call, Popen, PIPE
from pathlib import Path
import config
import logging

def parse_args():
    """
    Parse command-line arguments.
    """
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Align and filter FASTQ reads using minimap2 and samtools.")
    parser.add_argument('--config', required=True, type=str, help="Path to pipeline configuration file")
    parser.add_argument('--output', required=True, type=str, help="Path to output directory")
    return parser.parse_args()

def align_and_filter_reads(fastq, reference, output, threads, aligner_path):
    """
    Align and filter FASTQ reads using minimap2 and samtools.
    """
    bam_path = os.path.join(output, os.path.basename(fastq).replace(".fastq", ".bam"))
    sorted_bam_path = bam_path.replace(".bam", ".sorted.bam")

    # Use hyperparameterized minimap2 command
    p1 = Popen(f"{aligner_path} -ax splice -uf -k14 {reference} {fastq}".split(), stdout=PIPE)
    p2 = Popen(f"samtools sort -@ {threads} -o {sorted_bam_path}".split(), stdin=p1.stdout)
    p1.stdout.close()
    p2.communicate()

    check_call(f"samtools index {sorted_bam_path}".split())
    logging.info(f"Aligned and sorted BAM: {sorted_bam_path}")
    
    return sorted_bam_path

def main():
    """
    Main function to execute the alignment.
    """
    args = parse_args()
    config_file = args.config
    output = args.output
    cfg = config.load_config(config_file)

    logging.info("Starting read alignment.")
    sorted_bam_path = align_and_filter_reads(cfg['fastq'], cfg['reference'], Path(output), cfg['threads'], cfg['aligner_path'])
    logging.info("Read alignment completed.")

    # Save the sorted BAM path to the config file for later steps
    cfg['sorted_bam'] = str(sorted_bam_path)
    config.save_config(config_file, cfg)

if __name__ == "__main__":
    main()
