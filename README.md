# NanoRNA-ClusteringPipeline

This repository contains the NanoRNA-ClusteringPipeline, designed for analyzing Direct RNA sequencing data from raw Oxford Nanopore Technologies (ONT) FAST5 files. The pipeline includes steps for splitting multi-read FAST5 files, indexing reads, aligning and filtering FASTQ reads, clustering RNA reads, and estimating Poly(A) tail lengths, and managing the eventalign tool in raw reads by using a variety of tools. This specific repository works upon that basis to further speed things up using GPU-acceleration through appropiate alternatives to the tools used in the original repository. 

## Current Branch Steps to Consider:
1. NVIDIA Docker, and cloud instant run. 

## Table of Contents
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Docker](#docker)
- [Dependencies](#dependencies)
- [Pipeline Steps](#pipeline-steps)
- [Logging](#logging)
- [Acknowledgments](#acknowledgments)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)

## Installation

### Clone the Repository
```bash
git clone -b GPU_experimental https://github.com/sarodarte2/NanoRNA-ClusteringPipeline.git
cd NanoRNA-ClusteringPipeline
```
## Manual Pipeline-Running

### Run Setup Script
To set up the environment and install all dependencies, run the provided setup script twice (once for installation and the second will populate the paths for the dependencies whist confirming all programs have been installed:

```bash
./setup_pipeline.sh
./setup_pipeline.sh
```

## Configuration
The pipeline requires a configuration file in YAML format. If running the pipeline locally, change the paths in the yaml file for FastQ, FAST5, sequencing summary, and reference fasta file. Here is an example `pipeline_config.yaml`:
```yaml
# Path to the Minimap2 executable.
aligner_path: /path/to/minimap2

# Directory containing the input FAST5 files.
fast5: /path/to/fast5_directory

# Path to the input FASTQ file.
fastq: /path/to/input_fastq_file.fastq

# Path to the GeLuster executable.
geluster_path: /path/to/GeLuster/GeLuster

# Path to the multi_to_single_fast5 executable (from the ONT fast5 API).
multi_to_single_fast5_path: /path/to/multi_to_single_fast5

# Path to the Nanopolish executable.
nanopolish_path: /path/to/nanopolish/nanopolish

# Path to the f5c executable.
f5c_path: /path/to/f5c/f5c_x86_64_linux_cuda  # or f5c_x86_64_linux for CPU-only

# Directory where the pipeline outputs will be stored.
output: /path/to/pipeline_outputs

# Path to the PycoQC executable.
pycoqc_path: /path/to/pycoQC

# Path to the reference genome file.
reference: /path/to/reference_genome.fa

# Path to the Samtools executable.
samtools_path: /path/to/samtools

# Path to the sequencing summary file.
sequencing_summary: /path/to/sequencing_summary.txt

# Path to the sorted BAM file (output from the alignment step).
sorted_bam: /path/to/sorted_output.bam

# Number of threads to use for the operations.
threads: 10
```

### Manual Configuration
If you are running the pipeline manually using the scripts, you will need to update the configuration file with the paths to your input FAST5 files, FASTQ file, sequencing summary file from the basecalling, reference genome, and the number of threads. Make sure you save the file.

## Usage

### Running the Pipeline
```bash
./run_pipeline.sh
```
## Docker
You can also use Docker to run the pipeline in a containerized environment. Do note the f5c instant of the Docker build will not be GPU accelerated. We are considering making an NVIDIA-Docker appropiately but that requires extra setup. Build the Docker image using the provided Dockerfile:

```bash
docker build -t nanorna-clustering-pipeline .
```
To run the pipeline using Docker, set the required environment variables and run the container setting the paths for each of the files:

```bash
docker run -e FASTQ_PATH=/path/to/fastq -e FAST5_PATH=/path/to/fast5 -e REF_PATH=/path/to/reference -e SEQUENCING_SUMMARY=/path/to/sequencing_summary.txt -e CONFIG_PATH=/path/to/config/pipeline_config.yaml -e THREADS=10 nanorna-clustering-pipeline
```
## Dependencies
- Python 3
- ont-fast5-api
- Nanopolish
- Minimap2
- Samtools
- GeLuster
- PycoQC
- f5c

## Pipeline Steps
1. **Split FAST5 Files:** Converts multi-read FAST5 files into single-read FAST5 files.
2. **Index Reads:** Indexes reads from the FAST5 and FASTQ files using Nanopolish.
3. **Align and Filter Reads:** Aligns FASTQ reads to a reference genome using Minimap2 and sorts the alignments with Samtools.
4. **Generate PycoQC Report:** Generates a quality control report using PycoQC.
5. **Cluster Reads:** Clusters RNA reads using GeLuster, with support for clustering multiple samples.
6. **Estimate Poly(A) Tail Lengths:** Estimates the lengths of Poly(A) tails using Nanopolish.
7. **Event Alignment:** Aligns events using f5c, with support for GPU acceleration if CUDA is installed.

## Logging
A single log file is generated for each pipeline run, located in the 'logs' directory specified in the configuration file. The log file is named with the current date and time for easy identification.

## Acknowledgements
- [ont-fast5-api](https://github.com/nanoporetech/ont_fast5_api)
- [Nanopolish](https://github.com/jts/nanopolish)
- [minimap2](https://github.com/lh3/minimap2)
- [samtools](https://github.com/samtools/samtools)
- [GeLuster](https://github.com/GeLuster)
- [PycoQC](https://github.com/a-slide/pycoQC)
- [f5c](https://github.com/hasindu2008/f5c)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with any improvements or bug fixes.

## Contact

For any questions or issues, please contact [sarodarte2@miners.utep.edu](mailto:your-email@example.com).
