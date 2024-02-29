# Required modules
import json
import pandas as pd

m3u_filepaths_file = 'playlists/streamlit.m3u8'
GENRE_ANALYSIS_PATH = 'data/genre_predictions.csv'
METADATA_FILE_PATH = 'metadata/discogs-effnet-bs64-1.json'
OTHER_FEATURES_PATH = 'data/features.csv'

def load_genre_analysis():
    # Read discogs metadata json file to get the genre corresponding to each index
    with open(METADATA_FILE_PATH) as file:
        metadata_dict = json.load(file)
    genre_analysis_styles = metadata_dict["classes"]

    # Read the CSV file
    df = pd.read_csv(GENRE_ANALYSIS_PATH, header=None)

    # Set the first column as the index
    df.set_index(0, inplace=True)
    df.index.name = None

    # Select the 4th column and above
    df = df[df.columns[3:]]

    # Create a dictionary mapping old column names to new column names
    column_mapping = dict(zip(df.columns, genre_analysis_styles))

    # Rename the columns
    df.rename(columns=column_mapping, inplace=True)

    return df, genre_analysis_styles

def load_tempo_analysis():

    # Read the CSV file
    df = pd.read_csv(OTHER_FEATURES_PATH, header=None, usecols=[0, 1])

    # Set the first column as the index
    df.set_index(0, inplace=True)
    df.index.name = None

    # Rename the columns
    df.rename(columns={1: 'tempo'}, inplace=True)

    return df

def load_instrumental_analysis():
    # Read the CSV file
    df = pd.read_csv(OTHER_FEATURES_PATH, header=None, usecols=[0, 9])

    # Set the first column as the index
    df.set_index(0, inplace=True)
    df.index.name = None

    # Rename the columns
    df.rename(columns={9: 'Instrumental/Voice'}, inplace=True)

    return df

def load_danceability_analysis():
    # Read the CSV file
    df = pd.read_csv(OTHER_FEATURES_PATH, header=None, usecols=[0, 10])

    # Set the first column as the index
    df.set_index(0, inplace=True)
    df.index.name = None

    # Rename the columns
    df.rename(columns={10: 'danceability'}, inplace=True)

    return df

def load_arousal_valence_analysis():
    # Read the CSV file
    df = pd.read_csv(OTHER_FEATURES_PATH, header=None, usecols=[0, 11, 12])

    # Set the first column as the index
    df.set_index(0, inplace=True)
    df.index.name = None

    # Rename the columns
    df.rename(columns={11: 'arousal', 12: 'valence'}, inplace=True)

    return df

def load_key_scale_analysis():

    # Read the CSV file
    df = pd.read_csv(OTHER_FEATURES_PATH, header=None, usecols=[0, 2, 3, 4, 5, 6, 7])

    # Set the first column as the index
    df.set_index(0, inplace=True)
    df.index.name = None

    # Combine the key and scale columns
    df['keyTemperley'] = df[2] + ' ' + df[3]
    df['keyKrumhansl'] = df[4] + ' ' + df[5]
    df['keyEdma'] = df[6] + ' ' + df[7]

    # Drop the original key and scale columns
    df.drop(columns=[2, 3, 4, 5, 6, 7], inplace=True)

    return df
