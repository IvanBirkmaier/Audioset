import pandas as pd
import wave
import os
import torchaudio
import torchaudio.transforms as T


# Dataframe processing function
def testpipline_audiofiles(df: pd.DataFrame, log_path: str = "") -> pd.DataFrame:
    df = df.copy(deep=True)
    df["wav_duration"] = 0
    
    # Collect indices of rows to drop
    indices_to_drop = []
    
    for idx, row in df.iterrows():
        file_path = row["wav"]
        
        test_1, waveform, sr = test_loading_wav(file_path, log_path)
        if not test_1 or \
           not test_resampling_wav(file_path, log_path, waveform, sr) or \
           not test_fbank_wav(file_path, log_path, waveform, sr):
            indices_to_drop.append(idx)
        else:
            df.at[idx, "wav_duration"] = wav_duration(file_path, log_path)
    
    # Drop rows by index
    df.drop(index=indices_to_drop, inplace=True)
    return df


def test_loading_wav(file_path, log_path):
    try:
        waveform, sr = torchaudio.load(file_path)
    except Exception as e:
        log_dir = os.path.dirname(log_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        with open(log_path, "a") as log_file:
            log_file.write(f"Error while trying to load file: [{file_path}] Error message: {e}\n")
        return False, None, None
    return True, waveform, sr

def test_resampling_wav(file_path, log_path, waveform, sr) -> bool:
    try:
        resampler = T.Resample(sr, 16000)
        waveform = resampler(waveform)
        sr = 16000  # Setze die Sample-Rate auf 16kHz
    except Exception as e:
        log_dir = os.path.dirname(log_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        with open(log_path, "a") as log_file:
            log_file.write(f"Error while trying to resample file: [{file_path}] Error message: {e}\n")
        return False
    return True

def test_fbank_wav(file_path, log_path, waveform, sr) -> bool:
    try:
        fbank = torchaudio.compliance.kaldi.fbank(
            waveform,
            htk_compat=True,
            sample_frequency=sr,
            use_energy=False,
            window_type="hanning",
            num_mel_bins=128,
            dither=0.0,
            frame_shift=10,
        )
    except Exception as e:
        log_dir = os.path.dirname(log_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        with open(log_path, "a") as log_file:
            log_file.write(f"Error while creating FBANKs for file: [{file_path}] Error message: {e}\n")
        return False
    return True


def wav_duration(file_path, log_path):
    try:
        # Überprüfen, ob die Datei beschädigt ist
        with wave.open(file_path, "rb") as wav_file:
                        frames = wav_file.getnframes()
                        rate = wav_file.getframerate()
                        duration = frames / float(
                            rate
                        )  # Berechnung der Dauer in Sekunden
                        
    except Exception as e:
            log_dir = os.path.dirname(log_path)
            if not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)

            with open(log_path, "a") as log_file:
                log_file.write(f"Error while open file with wave lib for file: [{file_path}] Error message: {e}\n")
            return 0
    return duration