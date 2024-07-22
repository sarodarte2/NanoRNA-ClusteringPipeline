#!/bin/bash

# Ensure required environment variables are set
if [ -z "$FASTQ_PATH" ] || [ -z "$FAST5_PATH" ] || [ -z "$REF_PATH" ] || [ -z "$SEQUENCING_SUMMARY" ] || [ -z "$CONFIG_PATH" ] || [ -z "$THREADS" ]; then
  echo "Required environment variables are not set."
  exit 1
fi

# Paths to executables
NANOPOLISH_PATH=$(find /root/NanoRNA-ClusteringPipeline/tools/nanopolish -name nanopolish)
MINIMAP2_PATH=$(which minimap2)
SAMTOOLS_PATH=$(which samtools)
PYCOQC_PATH=$(which pycoQC)
MULTI_TO_SINGLE_FAST5_PATH=$(which multi_to_single_fast5)
GELUSTER_PATH=$(find /root/NanoRNA-ClusteringPipeline/tools/GeLuster -name GeLuster)

# Update the configuration file with the correct paths
sed -i "s|nanopolish_path:.*|nanopolish_path: $NANOPOLISH_PATH|" $CONFIG_PATH
sed -i "s|aligner_path:.*|aligner_path: $MINIMAP2_PATH|" $CONFIG_PATH
sed -i "s|geluster_path:.*|geluster_path: $GELUSTER_PATH|" $CONFIG_PATH
sed -i "s|samtools_path:.*|samtools_path: $SAMTOOLS_PATH|" $CONFIG_PATH
sed -i "s|pycoqc_path:.*|pycoqc_path: $PYCOQC_PATH|" $CONFIG_PATH
sed -i "s|multi_to_single_fast5_path:.*|multi_to_single_fast5_path: $MULTI_TO_SINGLE_FAST5_PATH|" $CONFIG_PATH
sed -i "s|fastq:.*|fastq: $FASTQ_PATH|" $CONFIG_PATH
sed -i "s|fast5:.*|fast5: $FAST5_PATH|" $CONFIG_PATH
sed -i "s|reference:.*|reference: $REF_PATH|" $CONFIG_PATH
sed -i "s|sequencing_summary:.*|sequencing_summary: $SEQUENCING_SUMMARY|" $CONFIG_PATH
sed -i "s|threads:.*|threads: $THREADS|" $CONFIG_PATH

# Execute the pipeline
python3 scripts/run_pipeline.py --config $CONFIG_PATH
