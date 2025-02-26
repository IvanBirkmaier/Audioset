import pandas as pd
import json
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Enviroment variable
__PATH_TO_REPOSITORY__ = os.getenv("PATH_TO_REPOSITORY")


# Paths for diffrent data-files + Labels
__PATHS__ = {
    "evaluation": {
        "save_path": f"{__PATH_TO_REPOSITORY__}/datafiles/ast/eval_data.json",
        "preprocessed_path": f"{__PATH_TO_REPOSITORY__}/csv/eval/preprocessed_segment/preprocessed_eval_segments.csv"
    },
    "balanced": {
        "save_path": f"{__PATH_TO_REPOSITORY__}/datafiles/ast/balanced_train_data.json",
        "preprocessed_path": f"{__PATH_TO_REPOSITORY__}/csv/balanced_train/preprocessed_segment/preprocessed_balanced_train_segments.csv"
    },
    "unbalanced": {
        "save_path": f"{__PATH_TO_REPOSITORY__}/datafiles/ast/unbalanced_train_data.json",
        "preprocessed_path": f"{__PATH_TO_REPOSITORY__}/csv/unbalanced_train/preprocessed_segment/preprocessed_unbalanced_train_segments.csv"
    }
}


def prepaire_dataset(data_path="", save_path=""):
    # Creates dataframe
    df = pd.read_csv(data_path)
    # Creates a new dataframe with only the 'positive_labels' and 'wav' feature for audioset training
    df = df[['positive_labels', 'wav']]
    # Renames 'positive_labels' into the write name which is needed by the ast repo 
    df = df.rename(columns={'positive_labels': 'labels'})
    # Creates json-file
    json_data = {'data': df.to_dict(orient='records')}

    # Creates dir if not already exists for saving the files
    save_dir = os.path.dirname(save_path)
    if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    
    # Safes json which is needed for train the trainsformer
    with open(save_path, 'w') as f:
        json.dump(json_data, f, indent=4)



def main():
    for _, paths in __PATHS__.items():
        # I used the preprocessed path for generating the json files and save it to the save path
        prepaire_dataset(paths["preprocessed_path"], paths["save_path"])


if __name__ == "__main__":
    main()
