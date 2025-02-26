import os
from dotenv import load_dotenv
from pipeline import pipeline
from audio_tests import testpipline_audiofiles

# Load .env file
load_dotenv()

# Enviroment variable
__PATH_TO_REPOSITORY__ = os.getenv("PATH_TO_REPOSITORY")

# path to audioset ontology
__ONTOLOGY_JSON_PATH__ = f"{__PATH_TO_REPOSITORY__}/data/labels/ontology/ontology.json"

# Paths for diffrent data-files + Labels
__PATHS__ = {
    "evaluation": {
        "wave_path": f"{__PATH_TO_REPOSITORY__}/data/audio/wav/eval_segments",
        "label_path": f"{__PATH_TO_REPOSITORY__}/data/labels/eval_segments.csv",
        "save_path": f"{__PATH_TO_REPOSITORY__}/csv/eval/full_segment/full_eval_segments.csv",
        "log_path":  f"{__PATH_TO_REPOSITORY__}/csv/eval/logs/audio_files_error_logs.txt",
        "preprocessed_path": f"{__PATH_TO_REPOSITORY__}/csv/eval/preprocessed_segment/preprocessed_eval_segments.csv"
    },
    "balanced": {
        "wave_path": f"{__PATH_TO_REPOSITORY__}/data/audio/wav/balanced_train_segments",
        "label_path": f"{__PATH_TO_REPOSITORY__}/data/labels/balanced_train_segments.csv",
        "save_path": f"{__PATH_TO_REPOSITORY__}/csv/balanced_train/full_segment/full_balanced_train_segments.csv",
        "log_path":  f"{__PATH_TO_REPOSITORY__}/csv/balanced_train/logs/audio_files_error_logs.txt",
        "preprocessed_path": f"{__PATH_TO_REPOSITORY__}/csv/balanced_train/preprocessed_segment/preprocessed_balanced_train_segments.csv"
    },
    "unbalanced": {
        "wave_path": f"{__PATH_TO_REPOSITORY__}/data/audio/wav/unbalanced_train_segments",
        "label_path": f"{__PATH_TO_REPOSITORY__}/data/labels/unbalanced_train_segments.csv",
        "save_path": f"{__PATH_TO_REPOSITORY__}/csv/unbalanced_train/full_segment/full_unbalanced_train_segments.csv",       
        "log_path":  f"{__PATH_TO_REPOSITORY__}/csv/unbalanced_train/logs/audio_files_error_logs.txt",
        "preprocessed_path": f"{__PATH_TO_REPOSITORY__}/csv/unbalanced_train/preprocessed_segment/preprocessed_unbalanced_train_segments.csv"
    }
}

def main():
    for _, paths in __PATHS__.items():
        df = pipeline(paths["wave_path"], paths["label_path"], paths["save_path"], __ONTOLOGY_JSON_PATH__)
        df = testpipline_audiofiles(df, paths["log_path"])

        save_dir = os.path.dirname(paths["preprocessed_path"])
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        df.to_csv(paths["preprocessed_path"], index=False)

if __name__ == "__main__":
    main()
