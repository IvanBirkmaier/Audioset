import os
import json
import pandas as pd


def pipeline(wave_path="", label_path="", save_path="", __ONTOLOGY_JSON_PATH__=""):
    """
    Processes audio segment files, labels, and ontology data to generate a consolidated CSV file
    containing existing audio files with their corresponding labels and label names.

    Parameters:
        wave_path (str): Path to the directory containing audio files (e.g., WAV files).
        label_path (str): Path to the CSV file containing labels for evaluation segments.
        ontology_json_path (str): Path to the JSON file containing ontology data (ID-to-name mapping).
        save_path (str): Path to save the resulting CSV file.

    Steps:
        1. Iterates through the `wave_path` directory and gathers file paths and names.
        2. Cleans file names by removing prefixes and extensions (e.g., "Y" prefix, ".wav").
        3. Merges the audio file data with the labels using a common identifier (e.g., YTID).
        4. Filters out non-existent audio files from the labels.
        5. Adds two new columns:
            - `positive_labels_list`: A list of label IDs from the `positive_labels` column.
            - `positive_labels_names`: A list of human-readable label names mapped from ontology.
        6. Saves the resulting DataFrame as a CSV file at the specified `save_path`.

    Returns:
        None: The function saves the resulting CSV to `save_path`.
    """
    # List to store file paths and names
    file_data = []

    # Traverse the directory and collect file paths and names
    for root, _, files in os.walk(wave_path):
        for file in files:
            # Construct the full file path
            file_path = os.path.join(root, file)
            # Append file path and name to the list
            file_data.append({"file_path": file_path, "file_name": file})

    # Create a DataFrame from the file list
    file_df = pd.DataFrame(file_data, columns=["file_path", "file_name"])

    # Clean the file names (remove 'Y' prefix and '.wav' extension)
    file_df["file_name"] = (
        file_df["file_name"]
        .str.replace(r"^Y", "", regex=True)
        .str.replace(r"\.wav$", "", regex=True)
    )

    # Load the label data from the CSV file
    label_df = load_data(label_path)

    # Merge the audio file data with the labels DataFrame
    label_df = pd.merge(
        label_df, file_df, left_on="YTID", right_on="file_name", how="left"
    )

    # Drop unnecessary columns and rename columns for clarity
    label_df = label_df.drop(columns=["file_name"])
    label_df = label_df.rename(columns={"file_path": "wav"})

    # Filter rows where the audio file exists
    existing_wav_df = label_df[label_df["wav"].notna()]

    # Load ontology data from the JSON file
    with open(__ONTOLOGY_JSON_PATH__, "r") as f:
        json_data = json.load(f)

    # Create a mapping from ID to Name using ontology data
    id_to_name = {obj["id"]: obj["name"] for obj in json_data}

    # Add a column with the list of positive labels
    existing_wav_df["positive_labels_list"] = existing_wav_df[
        "positive_labels"
    ].str.split(",")

    # Add a column with the human-readable label names for each positive label
    existing_wav_df["positive_labels_names"] = existing_wav_df[
        "positive_labels_list"
    ].apply(
        lambda label_list: [id_to_name.get(label, "Unknown") for label in label_list]
    )

    # Ensure the directory for the save path exists
    save_dir = os.path.dirname(save_path)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Save the resulting DataFrame as a CSV file
    existing_wav_df.to_csv(save_path, index=False)
    
    return existing_wav_df


def load_data(file_path):
    """
    Loads and processes data from a file, transforming it into a clean pandas DataFrame.

    Parameters:
        file_path (str): Path to the file to be loaded.

    Returns:
        pd.DataFrame: A cleaned DataFrame with columns ['YTID', 'start_seconds', 'end_seconds', 'positive_labels'].

    Steps:
        1. Reads the file line by line into a list of strings.
        2. Drops unnecessary header rows.
        3. Splits raw data into separate columns based on commas.
        4. Cleans up whitespace and extraneous characters from the data.
        5. Renames columns to meaningful names for further processing.
    """

    # Read the file as a list of lines (each line as a string)
    with open(file_path, "r") as file:
        data = file.readlines()

    # Create a DataFrame from the list of lines, with one column called "raw_data"
    df = pd.DataFrame(data, columns=["raw_data"])

    # Drop the first three rows (assumed to be headers or irrelevant information)
    df = df.drop([0, 1, 2])
    df.reset_index(drop=True, inplace=True)  # Reset the index after dropping rows

    # Split the 'raw_data' column by commas into separate columns (max 4 parts)
    df = df["raw_data"].str.split(",", n=3, expand=True)

    # Rename the columns for clarity
    df.columns = ["YTID", "start_seconds", "end_seconds", "positive_labels"]

    # Strip unnecessary whitespace from all columns (object dtype only)
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # Remove double quotes and any spaces from the 'positive_labels' column
    df["positive_labels"] = (
        df["positive_labels"]
        .str.replace('"', "", regex=False)
        .str.replace(" ", "", regex=False)
    )

    return df
