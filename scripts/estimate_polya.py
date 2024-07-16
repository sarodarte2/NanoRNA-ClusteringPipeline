#!/usr/bin/env python3
"""
Estimate PolyA tail lengths using nanopolish.
"""

import os
import sys
import yaml
from pathlib import Path
from subprocess import check_call, CalledProcessError

def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

def setup_vbz_plugin():
    vbz_dir = os.path.expanduser("~/local/hdf5/lib/plugin")
    os.environ["HDF5_PLUGIN_PATH"] = vbz_dir
    print(f"HDF5_PLUGIN_PATH set to {vbz_dir}")

def estimate_polya(fastq, bam, reference, output, threads, nanopolish_path):
    output_file = output / "polya_results.tsv"
    env = os.environ.copy()
    env["HDF5_PLUGIN_PATH"] = os.environ.get("HDF5_PLUGIN_PATH")
    with open(output_file, "w") as output_handle:
        try:
            check_call(
                f"{nanopolish_path} polya --threads={threads} --reads={fastq} --bam={bam} --genome={reference}".split(),
                stdout=output_handle,
                env=env
            )
            print(f"Poly-A tail estimation completed. Results saved to {output_file}")
        except CalledProcessError as e:
            print(f"Nanopolish polya failed with exit status {e.returncode}")
            print(f"Command: {e.cmd}")
            raise

def main():
    config_file = sys.argv[2]
    output = Path(sys.argv[4])

    cfg = load_config(config_file)

    # Setup VBZ plugin
    setup_vbz_plugin()

    estimate_polya(cfg['fastq'], cfg['sorted_bam'], cfg['reference'], output, cfg['threads'], cfg['nanopolish_path'])

if __name__ == "__main__":
    main()
