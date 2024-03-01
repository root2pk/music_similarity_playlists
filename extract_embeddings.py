"""
This script extracts embeddings from audio files and writes them to a CSV file.

"""


from tqdm import tqdm
import methods as m
import pandas as pd
import numpy as np

# Set file path
DISCOGS_EMBEDDINGS_PATH = 'data/discogs_effnet_embeddings.csv'
MUSICNN_EMBEDDINGS_PATH = 'data/musicnn_embeddings.csv'
AUDIOFILES_PATH = "audio"

# Initialise essentia classes and load genre metadata
ess = m.EssentiaClasses()

# Search for audio files in the audiofiles directory
audio_files = m.search_audio_files(AUDIOFILES_PATH)

# Initialse embeddings files and clear them
open(DISCOGS_EMBEDDINGS_PATH, 'w').close()
open(MUSICNN_EMBEDDINGS_PATH, 'w').close()

# Exract embeddings for each audio file and write to CSV
pbar = tqdm(audio_files)
for audio_file in pbar:
    pbar.set_description(f"Extracting embeddings for {audio_file}")

    # Load audio file and extract embeddings
    audio_stereo, audio_mono = m.load_audio_file(audio_file)
    discogsEmbeddings = ess.getDiscogsEmbeddings(audio_mono)
    musicnnEmbeddings = ess.getMusiCNNEmbeddings(audio_mono)

    # Average embeddings
    discogsEmbeddings = discogsEmbeddings.mean(axis=0)
    musicnnEmbeddings = musicnnEmbeddings.mean(axis=0)

    # Write embeddings to CSV file
    df = pd.DataFrame([np.concatenate(([audio_file], discogsEmbeddings))])
    df.to_csv(DISCOGS_EMBEDDINGS_PATH, mode='a', header=False, index=False)

    df = pd.DataFrame([np.concatenate(([audio_file], musicnnEmbeddings))])
    df.to_csv(MUSICNN_EMBEDDINGS_PATH, mode='a', header=False, index=False)

print("Finished analyzing all audio files")