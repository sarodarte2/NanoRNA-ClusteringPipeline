# NanoRNA-ClusteringPipeline
This repository contains the NanoRNA-ClusteringPipeline, designed for analyzing Direct RNA sequencing data from raw Oxford Nanopore Technologies (ONT) FAST5 files. The pipeline includes steps for splitting multi-read FAST5 files, indexing reads, aligning and filtering FASTQ reads, and clustering RNA reads using a variety of tools.

## Table of Contents
- [Installation](#installation)
- [Docker](#docker)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Pipeline Steps](#pipeline-steps)
- [Configuration](#configuration)
- [Logging](#logging)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contributing](#contributing)
- [Contact](#contact)

## Installation

### Clone the Repository
```bash
git clone https://github.com/sarodarte2/NanoRNA-ClusteringPipeline.git
cd NanoRNA-ClusteringPipeline
```

### Set Up a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.
```bash
python3 -m venv env
source env/bin/activate
```

### Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

Install additional tools:
- [ont-fast5-api](https://github.com/nanoporetech/ont_fast5_api)
  ```bash
  pip install ont-fast5-api
  ```

- [Nanopolish](https://github.com/jts/nanopolish)
  ```bash
  git clone --recursive https://github.com/jts/nanopolish.git
  cd nanopolish
  make
  export PATH=$PATH:$(pwd)
  ```

- [minimap2](https://github.com/lh3/minimap2)
  ```bash
  git clone https://github.com/lh3/minimap2
  cd minimap2
  make
  export PATH=$PATH:$(pwd)
  ```

- [samtools](https://github.com/samtools/samtools)
  ```bash
  sudo apt-get install samtools
  ```

- [GeLuster](https://github.com/GeLuster)
  ```bash
  git clone https://github.com/GeLuster/GeLuster.git
  cd GeLuster/src
  make release
  export PATH=$PATH:$(pwd)
  ```

- [PycoQC](https://github.com/a-slide/pycoQC)
  ```bash
  pip install pycoqc
  ```
### Configuration

The pipeline requires a configuration file in YAML format. Here is an example `pipeline_config.yaml`:

```yaml
fast5: /path/to/your/fast5/files
fastq: /path/to/your/combined.fastq
reference: /path/to/your/reference.fasta
output: /path/to/output/directory
multi_to_single_fast5_path: /path/to/multi_to_single_fast5
nanopolish_path: /path/to/nanopolish
aligner_path: /path/to/minimap2
pycoqc_path: /path/to/pycoQC
geluster_path: /path/to/Geluster
sequencing_summary: /path/to/sequencing_summary.txt #This file is obtained from the basecalling.
bam: path/to/bam.bam # This file is obtained from original basecalling to reference sequence.
threads: 4 # Default threads
```


## Usage

### Running the Pipeline
To run the pipeline, use the following command:
```bash
python3 run_pipeline.py --config /path/to/your/pipeline_config.yaml
```

## Pipeline Steps

1. **Split FAST5 Files**: Converts multi-read FAST5 files into single-read FAST5 files.
2. **Index Reads**: Indexes reads from the FAST5 and FASTQ files using Nanopolish.
3. **Align and Filter Reads**: Aligns FASTQ reads to a reference genome using Minimap2 and sorts the alignments with Samtools.
4. **Cluster Reads**: (Optional) Clusters RNA reads using GeLuster, with support for clustering multiple samples.
5. **Generate MultiQC Report**: Compiles a comprehensive report using MultiQC.
6. **Data Processing**: (Optional) Basic statistical analysis of data with plotting.

## Logging

A single log file is generated for each pipeline run, located in the `logs` directory specified in the configuration file. The log file is named with the current date and time for easy identification.

## Dependencies

Ensure all the required tools are installed and accessible in your system's PATH:
- Python 3
- ont-fast5-api
- Nanopolish
- Minimap2
- Samtools
- GeLuster
- PycoQC

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [ont-fast5-api](https://github.com/nanoporetech/ont_fast5_api)
- [Nanopolish](https://github.com/jts/nanopolish)
- [minimap2](https://github.com/lh3/minimap2)
- [samtools](https://github.com/samtools/samtools)
- [GeLuster](https://github.com/GeLuster)
- [PycoQC][(https://github.com/ewels/MultiQC)](https://github.com/a-slide/pycoQC)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with any improvements or bug fixes.

## Contact

For any questions or issues, please contact [sarodarte2@miners.utep.edu](mailto:your-email@example.com).
