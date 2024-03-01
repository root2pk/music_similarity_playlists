"""
This app uses embeddings from two different models (DiscogsEfnet and MusiCNN) to create playlists based on audio similarity.

The embeddings are computed using the following models:
- DiscogsEfnet: A model trained on the Discogs dataset using the EfficientNet architecture.
- MusiCNN: A model trained on the Million Song Dataset using the MusiCNN architecture.

You can select a query track from the list or input a track name. The app will then display the top 10 similar tracks based on the selected query track.

The app uses cosine similarity to compute the similarity between the query track and the rest of the tracks in the dataset.

The app also provides the option to play the selected track and create playlists based on the top similar tracks.

"""


import streamlit as st
import utils as ut
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# File paths
DISCOGS_EMBEDDINGS_PATH = 'data/discogs_effnet_embeddings.csv'
MUSICNN_EMBEDDINGS_PATH = 'data/musicnn_embeddings.csv'
AUDIO_PATH = 'audio'

# Load discogs and musicnn embeddings as 2D numpy arrays
discogs_embeddings = pd.read_csv(DISCOGS_EMBEDDINGS_PATH, header=None).to_numpy()[:, 1:]
musicnn_embeddings = pd.read_csv(MUSICNN_EMBEDDINGS_PATH, header=None).to_numpy()[:, 1:]

# Compute similarity matrices
similarity_matrix_discogs = cosine_similarity(discogs_embeddings)
similarity_matrix_musicnn = cosine_similarity(musicnn_embeddings)

# Audio list is first column of discogs embeddings csv
audio_list = pd.read_csv(DISCOGS_EMBEDDINGS_PATH, header=None, usecols=[0])[0].tolist()

## MAIN PAGE ## -----------------------------------------------------------------------------------------------
st.write('# Create playlists based on audio similarlity')
st.subheader('This app uses embeddings from two different models (DiscogsEfnet and MusiCNN) to create playlists based on audio similarity.')

# Select query track from list or input a track name
track_select = None
st.write('## Select a query track from the list or input a track name')
use_input_box = st.checkbox('Enter a track name instead of selecting from the list')

# If input box is checked, show input box, else show select box
if use_input_box:
    track_input = st.text_input('Enter a track name (end with file extension .mp3 etc.)')
    if track_input:
        track_select = next((track for track in audio_list if track.endswith(track_input)), None)
else:
    track_select = st.selectbox('Select a track', audio_list)

# If a track is selected, show the track and create playlists
if track_select:
    # Show the selected track
    st.write('Selected track:', track_select)
    # Play track
    st.audio(track_select, format="audio/mp3", start_time=0)

    if st.button("RUN"):
        # Get the index of the selected track
        track_index = audio_list.index(track_select)

        # Compute similarity scores
        discogs_similarities = similarity_matrix_discogs[track_index]
        musicnn_similarities = similarity_matrix_musicnn[track_index]

        # Sort the tracks based on similarity scores
        discogs_sorted_indices = discogs_similarities.argsort()[::-1]
        musicnn_sorted_indices = musicnn_similarities.argsort()[::-1]

        # Display the top 10 similar tracks, ignore first track (it's the query track)
        st.write('## Discogs embeddings')
        ut.display_tracks([audio_list[i] for i in discogs_sorted_indices[1:]], max_tracks=10, shuffle=False, m3u_filepath='playlists/discogs_playlist.m3u')
        st.write('## Musicnn embeddings')
        ut.display_tracks([audio_list[i] for i in musicnn_sorted_indices[1:]], max_tracks=10, shuffle=False, m3u_filepath='playlists/musicnn_playlist.m3u')

else:
    st.write('No track/incorrect track selected')