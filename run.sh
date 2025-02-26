#!/bin/bash
#SBATCH --job-name="audioset_preprocessing"
#SBATCH --output=./slurm/%j/log.txt
#SBATCH --error=./slurm/%j/error.txt

# Creates a subfolder with your Slurm job ID
mkdir -p ./slurm/$SLURM_JOB_ID

set -x
source ~/miniconda3/etc/profile.d/conda.sh   # Makes conda available
conda activate audioset_preprocessing

# --- Parse Flags ---
pipeline=false
download=false
preprocess=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --pipeline)
      pipeline=true
      shift
      ;;
    --download)
      download=true
      shift
      ;;
    --preprocess)
      preprocess=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      shift
      ;;
  esac
done

# --- Run Commands Based on Flags ---

if [ "$pipeline" = true ]; then
  echo "Running pipeline: download + preprocessing..."
  bash ./src/download/download.sh
  python ./src/preprocessing/preprocessing.py
fi

if [ "$download" = true ]; then
  echo "Running download only..."
  bash ./src/download/download.sh
fi

if [ "$preprocess" = true ]; then
  echo "Running preprocessing only..."
  python ./src/preprocessing/preprocessing.py
fi

# Move Slurm output/error files into the job-specific subfolder
mv slurm-${SLURM_JOB_ID}.out ./slurm/$SLURM_JOB_ID/ 2>/dev/null || true
mv slurm-${SLURM_JOB_ID}.err ./slurm/$SLURM_JOB_ID/ 2>/dev/null || true
