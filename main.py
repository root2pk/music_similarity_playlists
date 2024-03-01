"""
This script is used to analyze audio files and extract features from them. The features are then written to a CSV file.

"""


import pandas as pd
from tqdm import tqdm
import methods as m

# Set file paths
AUDIOFILES_PATH = "audio"
FEATURES_FILE_PATH = 'data/features.csv'
GENRE_PREDICTIONS_FILE_PATH = 'data/genre_predictions.csv'
METADATA_FILE_PATH = 'metadata/discogs-effnet-bs64-1.json'
GENRE_COUNTS_FILE_PATH = 'data/genre_counts.tsv'

# Initialise essentia classes and load genre metadata
ess = m.EssentiaClasses()
ess.load_genre_metadata(METADATA_FILE_PATH)

def analyze_audio_files(audio_files):

    pbar = tqdm(audio_files)
    for audio_file in pbar:
        pbar.set_description(f"Analyzing {audio_file}")

        # Load audio file and extract features
        audio_stereo, audio_mono = m.load_audio_file(audio_file)
        ess.extract_features(audio_mono, audio_stereo)

        # Write features to CSV file
        features_dict = ess.write_features_dict(audio_file)
        df_features = pd.DataFrame([features_dict])
        df_features.to_csv(FEATURES_FILE_PATH, mode='a', header=False, index=False)
        
        # Write genre predictions to CSV file
        genre_predictions_dict = ess.write_genre_dict(audio_file)
        df_genre_predictions = pd.DataFrame([genre_predictions_dict])
        df_genre_predictions.to_csv(GENRE_PREDICTIONS_FILE_PATH, mode='a', header=False, index=False)

    print("Finished analyzing all audio files")

def main():
    # Search for audio files in the audiofiles directory
    audio_files = m.search_audio_files(AUDIOFILES_PATH)

    # Initialse features.csv and genre_predicitons.csv and clear them
    open(FEATURES_FILE_PATH, 'w').close()
    open(GENRE_PREDICTIONS_FILE_PATH, 'w').close()

    # Analyze audio files and write features to CSV
    analyze_audio_files(audio_files)

    print("Writing genre counts to genre_counts.tsv...")
    # Extract specific genre predictions from genre_predictions.csv
    genre_df = pd.read_csv(GENRE_PREDICTIONS_FILE_PATH, usecols=[2], header=None)
    genre_df.columns = ['Genre']

    # Save the extracted genre predictions and number of occurrences to a new TSV file
    genre_df['Genre'].value_counts().to_csv(GENRE_COUNTS_FILE_PATH, sep='\t', header=['Count'])

if __name__ == "__main__":
    main()
