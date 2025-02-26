#!/bin/bash
#SBATCH --job-name=download_audioset                    # Name of the job
#SBATCH --output=/logs/output_download_audioset_%j.out  # File for standard output
#SBATCH --error=/logs/error_download_audioset_%j.err    # File for error output

# Ensure /logs directory exists for SLURM job logs
mkdir -p /logs

# Start the script
echo "Starting AudioSet download and processing script..."

########################################################################################################################################################################################################
########################################################################################################################################################################################################
########################################################################################################################################################################################################

# DOWNLOAD AUDIOSET ONTOLOGY REPO FILES:

# Function to download and unzip a specific repository
download_and_unzip_repo() {
  local repo_url="https://github.com/audioset/ontology"
  local target_folder="../../data/labels"

  echo "Starting repository download and extraction..."

  # Ensure the target directory exists
  mkdir -p "$target_folder"

  # Clone the repository
  if git clone "$repo_url" "$target_folder"; then
    echo "Successfully cloned repository into $target_folder."
  else
    echo "Error: Failed to clone repository from $repo_url."
    exit 1
  fi

  # Check for and unzip any .zip files in the target folder
  echo "Checking for zip files in $target_folder..."
  if find "$target_folder" -name "*.zip" -exec unzip -o {} -d "$target_folder" \;; then
    echo "All zip files in $target_folder have been extracted."
  else
    echo "No zip files found or extraction failed."
  fi

  echo "Repository processing completed."
}

# Call the function
download_and_unzip_repo

########################################################################################################################################################################################################
########################################################################################################################################################################################################
########################################################################################################################################################################################################

# DOWNLOAD LABEL FILES:

echo "Downloading labels CSV files..."
# Target directory
LABELS_DIR="../../data/labels"
# Create the target directory if it doesn't exist
mkdir -p "$LABELS_DIR"
# Base URL
BASE_URL="http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv"
# List of CSV files to download
FILES=(
  "eval_segments.csv"
  "balanced_train_segments.csv"
  "unbalanced_train_segments.csv"
)
# Download each file
for FILE in "${FILES[@]}"; do
  echo "Downloading $FILE..."
  wget -q -P "$LABELS_DIR" "$BASE_URL/$FILE"
  if [ $? -eq 0 ]; then
    echo "$FILE downloaded successfully."
  else
    echo "Failed to download $FILE."
  fi
done
echo "All labels have been successfully downloaded to $LABELS_DIR."

########################################################################################################################################################################################################
########################################################################################################################################################################################################
########################################################################################################################################################################################################

# DOWNLOAD AUDIO FILES:

echo "Downloading audio files..."
# Function to download and process a single zip file
process_file() {
  local BASE_URL="$1"
  local FILE="$2"
  local DOWNLOAD_DIR="$3"

  # Create the target directory if it doesn't exist
  mkdir -p "$DOWNLOAD_DIR"

  # Define the target file path
  local TARGET_FILE="${DOWNLOAD_DIR}/${FILE}"

  echo "Downloading $FILE..."
  wget -O "$TARGET_FILE" "${BASE_URL}/${FILE}?download=true"

  # Create a temporary directory for unzipping
  local TEMP_DIR="${DOWNLOAD_DIR}/temp_${FILE%_full.zip}"
  mkdir -p "$TEMP_DIR"

  echo "Unzipping $FILE into $TEMP_DIR..."
  unzip -q "$TARGET_FILE" -d "$TEMP_DIR"

  # Move the largest directory from TEMP_DIR to target
  local MAX_DIR=$(find "$TEMP_DIR" -type d -exec bash -c 'echo "$(find "{}" -type f | wc -l) {}"' \; | sort -rn | head -n 1 | awk '{print $2}')
  if [ -n "$MAX_DIR" ]; then
    mv "$MAX_DIR" "${DOWNLOAD_DIR}/${FILE%_full.zip}"
    echo "Moved largest directory ($MAX_DIR) to ${DOWNLOAD_DIR}/${FILE%_full.zip}"
  else
    echo "No files found to move for $FILE"
  fi

  # Cleanup temporary files
  rm -rf "$TEMP_DIR" "$TARGET_FILE"
  echo "Cleanup complete for $FILE"
}

# Define directories and base URLs
UNBALANCED_DOWNLOAD_DIR="../../data/audio/wav/unbalanced_train_segments"
UNBALANCED_BASE_URL="https://huggingface.co/datasets/confit/audioset-full/resolve/main/unbalanced"

BALANCED_DOWNLOAD_DIR="../../data/audio/wav/balanced_train_segments"
BALANCED_FILE="balanced_train_segments.zip"
BALANCED_BASE_URL="https://huggingface.co/datasets/confit/audioset-full/blob/main/balanced"

EVAL_DOWNLOAD_DIR="../../data/audio/wav/eval_segments"
EVAL_FILE="eval_segments.zip"
EVAL_BASE_URL="https://huggingface.co/datasets/confit/audioset-full/blob/main/eval"

# List of unbalanced training files
UNBALANCED_FILES=(
  "unbalanced_train_segments_part00_full.zip"
  "unbalanced_train_segments_part01_full.zip"
  "unbalanced_train_segments_part02_full.zip"
  "unbalanced_train_segments_part03_full.zip"
  "unbalanced_train_segments_part04_full.zip"
  "unbalanced_train_segments_part05_full.zip"
  "unbalanced_train_segments_part06_full.zip"
  "unbalanced_train_segments_part07_full.zip"
  "unbalanced_train_segments_part08_full.zip"
  "unbalanced_train_segments_part09_full.zip"
  "unbalanced_train_segments_part10_full.zip"
  "unbalanced_train_segments_part11_full.zip"
  "unbalanced_train_segments_part12_full.zip"
  "unbalanced_train_segments_part13_full.zip"
  "unbalanced_train_segments_part14_full.zip"
  "unbalanced_train_segments_part15_full.zip"
  "unbalanced_train_segments_part16_full.zip"
  "unbalanced_train_segments_part17_full.zip"
  "unbalanced_train_segments_part18_full.zip"
  "unbalanced_train_segments_part19_full.zip"
  "unbalanced_train_segments_part20_full.zip"
  "unbalanced_train_segments_part21_full.zip"
  "unbalanced_train_segments_part22_full.zip"
  "unbalanced_train_segments_part23_full.zip"
  "unbalanced_train_segments_part24_full.zip"
  "unbalanced_train_segments_part25_full.zip"
  "unbalanced_train_segments_part26_full.zip"
  "unbalanced_train_segments_part27_full.zip"
  "unbalanced_train_segments_part28_full.zip"
  "unbalanced_train_segments_part29_full.zip"
  "unbalanced_train_segments_part30_full.zip"
  "unbalanced_train_segments_part31_full.zip"
  "unbalanced_train_segments_part32_full.zip"
  "unbalanced_train_segments_part33_full.zip"
  "unbalanced_train_segments_part34_full.zip"
  "unbalanced_train_segments_part35_full.zip"
  "unbalanced_train_segments_part36_full.zip"
  "unbalanced_train_segments_part37_full.zip"
  "unbalanced_train_segments_part38_full.zip"
  "unbalanced_train_segments_part39_full.zip"
  "unbalanced_train_segments_part40_full.zip"
)

# Process unbalanced training files
for FILE in "${UNBALANCED_FILES[@]}"; do
  process_file "$UNBALANCED_BASE_URL" "$FILE" "$UNBALANCED_DOWNLOAD_DIR"
done

# Process the balanced training file
process_file "$BALANCED_BASE_URL" "$BALANCED_FILE" "$BALANCED_DOWNLOAD_DIR"

# Process the evaluation segments file
process_file "$EVAL_BASE_URL" "$EVAL_FILE" "$EVAL_DOWNLOAD_DIR"

echo "All files have been downloaded and processed."

for FILE in "${FILES[@]}"; do
  TARGET_FILE="${DOWNLOAD_DIR}/${FILE}"

  echo "Downloading $FILE..."
  wget -O "$TARGET_FILE" "$BASE_URL/$FILE?download=true"

  TEMP_DIR="${DOWNLOAD_DIR}/temp_${FILE%_full.zip}"
  mkdir -p "$TEMP_DIR"

  echo "Unzipping $FILE into $TEMP_DIR..."
  unzip -q "$TARGET_FILE" -d "$TEMP_DIR"

  # Move the largest directory from TEMP_DIR to target
  MAX_DIR=$(find "$TEMP_DIR" -type d -exec bash -c 'echo "$(find "{}" -type f | wc -l) {}"' \; | sort -rn | head -n 1 | awk '{print $2}')
  if [ -n "$MAX_DIR" ]; then
    mv "$MAX_DIR" "${DOWNLOAD_DIR}/${FILE%_full.zip}"
    echo "Moved largest directory ($MAX_DIR) to ${DOWNLOAD_DIR}/${FILE%_full.zip}"
  else
    echo "No files found to move for $FILE"
  fi

  # Cleanup
  rm -rf "$TEMP_DIR" "$TARGET_FILE"
  echo "Cleanup complete for $FILE"
done

echo "All AudioSet unbalanced training data has been downloaded and processed."



