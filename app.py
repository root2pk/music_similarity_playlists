"""
This app uses extracted features to build playlists.
Features to be used can be selected using the sidebar. The user can then filter through their requirements for each feature and create separate playlists.

The app uses the following features to create playlists:
- Genre
- Tempo
- Instrumental/Voice
- Danceability
- Arousal-Valence
- Key and Scale

"""

import streamlit as st
import utils as ut
import subprocess

# File paths
GENRE_ANALYSIS_PATH = 'data/genre_predictions.csv'
OTHER_FEATURES_PATH = 'data/features.csv'
METADATA_FILE_PATH = 'metadata/discogs-effnet-bs64-1.json'

# Sidebar options
playlist_options = ["Welcome", "Genre", "Tempo", "Instrumental/Voice", "Danceability", "Arousal-Valence", "Key and Scale"]
playlist_option = st.sidebar.radio("Navigate", playlist_options)


if playlist_option == "Welcome":

    st.write('## Welcome to the Audio Analysis Playlists App!')
    st.write('This app creates playlists based on audio analysis data.')
    st.write('Existing data from the [MusAV](https://drive.google.com/drive/folders/197MdMGGVGxqo3dSesk4Iln4N1pVyt1SX) collection has been loaded')
    st.write('Use the options on the sidebar to navigate to your desired features and create playlists')

    # Add vertical space
    st.write('\n\n\n\n\n\n')

    st.write('To use your own audio, add your collection to the "audio" directory and run the analysis scripts below')
    # Add vertical space
    st.write('\n\n')
    st.write('<span style="color:red;">WARNING: THIS WILL TAKE A WHILE (APPROX. 10 SECONDS PER MINUTE OF AUDIO)</span>', unsafe_allow_html=True)

    if st.button("Run analysis"):
        st.write('Running analysis, this will take a while')
        # Run the analysis scripts
        result = subprocess.run(["python3", "main.py"])
        st.write('Analysis complete!')

    st.write('After running the analysis, you can (optionally) plot feature distributions by clicking on the button below')
    st.write('\n\n')
    if st.button("Plot feature distributions"):

        st.write('Plotting feature distributions')
        # Run the analysis scripts
        result = subprocess.run(["python3", "stats.py"])
        st.write('Plots complete and saved to the "plots" directory!')

elif playlist_option in ["Genre", "Tempo", "Instrumental/Voice", "Danceability", "Arousal-Valence", "Key and Scale"]:

    # Load the analysis data
    if playlist_option == "Genre":
        genre_analysis, genre_analysis_styles = ut.load_genre_analysis()
    elif playlist_option == "Tempo":
        tempo_analysis = ut.load_tempo_analysis()
    elif playlist_option == "Instrumental/Voice":
        instrumental_analysis = ut.load_instrumental_analysis()
    elif playlist_option == "Danceability":
        danceability_analysis = ut.load_danceability_analysis()
    elif playlist_option == "Arousal-Valence":
        arousal_valence_analysis = ut.load_arousal_valence_analysis()
    elif playlist_option == "Key and Scale":
        key_scale_analysis = ut.load_key_scale_analysis()

    if playlist_option == "Genre":
        st.write('# Genre analysis playlist')
        st.write(f'Using analysis data from `{GENRE_ANALYSIS_PATH}`.')
        st.write('Loaded audio analysis for', len(genre_analysis), 'tracks.')

        st.write('## 🔍 Select')
        st.write('### By style')
        st.write('Style activation statistics:')
        st.write(genre_analysis.describe())

        style_select = st.multiselect('Select by style activations:', genre_analysis_styles)
        if style_select:
            # Show the distribution of activation values for the selected styles.
            st.write(genre_analysis[style_select].describe())

            style_select_str = ', '.join(style_select)
            style_select_range = st.slider(f'Select tracks with `{style_select_str}` activations within range:', value=[0.5, 1.])

        st.write('## 🔝 Rank')
        style_rank = st.multiselect('Rank by style activations (multiplies activations for selected styles):', genre_analysis_styles, [])

        st.write('## 🔀 Post-process')
        max_tracks = st.number_input('Maximum number of tracks (0 for all):', value=0)
        shuffle = st.checkbox('Random shuffle')

        if st.button("RUN"):
            st.write('## 🔊 Results')
            mp3s = list(genre_analysis.index)

            if style_select:
                genre_analysis_query = genre_analysis.loc[mp3s][style_select]

                result = genre_analysis_query
                for style in style_select:
                    result = result.loc[result[style] >= style_select_range[0]]
                st.write(result)
                mp3s = result.index

            if style_rank:
                genre_analysis_query = genre_analysis.loc[mp3s][style_rank]
                genre_analysis_query['RANK'] = genre_analysis_query[style_rank[0]]
                for style in style_rank[1:]:
                    genre_analysis_query['RANK'] *= genre_analysis_query[style]
                ranked = genre_analysis_query.sort_values(['RANK'], ascending=[False])
                ranked = ranked[['RANK'] + style_rank]
                mp3s = list(ranked.index)

                st.write('Applied ranking by audio style predictions.')
                st.write(ranked)

            ut.display_tracks(mp3s, max_tracks, shuffle, m3u_filepath='playlists/genre_playlist.m3u8')

    if playlist_option == "Tempo":

        min_tempo = tempo_analysis['tempo'].min()
        max_tempo = tempo_analysis['tempo'].max()

        st.write('# ⏳ Playlist by tempo')
        tempo_select = st.slider('Filter by tempo:', min_value=min_tempo, max_value=max_tempo, value=(min_tempo, max_tempo))
        st.write('## 🔝 Rank')
        tempo_rank = st.selectbox('Rank by tempo:', ['Ascending', 'Descending'])
        st.write('## 🔀 Post-process')
        max_tracks = st.number_input('Maximum number of tracks (0 for all):', value=0)
        shuffle = st.checkbox('Random shuffle')

        if st.button("RUN"):
            st.write('## 🔊 Results')
            mp3s = list(tempo_analysis.index)

            tempo_analysis_query = tempo_analysis.loc[mp3s]
            result = tempo_analysis_query
            result = result.loc[(result['tempo'] >= tempo_select[0]) & (result['tempo'] <= tempo_select[1])]
            st.write(result)
            mp3s = result.index

            if tempo_rank == 'Ascending':
                tempo_analysis_query = tempo_analysis.loc[mp3s]
                ranked = tempo_analysis_query.sort_values(['tempo'], ascending=[True])
                mp3s = list(ranked.index)
                st.write('Applied ranking by tempo.')
                st.write(ranked)
            elif tempo_rank == 'Descending':
                tempo_analysis_query = tempo_analysis.loc[mp3s]
                ranked = tempo_analysis_query.sort_values(['tempo'], ascending=[False])
                mp3s = list(ranked.index)
                st.write('Applied ranking by tempo.')
                st.write(ranked)

            ut.display_tracks(mp3s, max_tracks, shuffle, m3u_filepath='playlists/tempo_playlist.m3u8')

    if playlist_option == "Instrumental/Voice":

        st.write('# 🎸 Playlist by instrumental/voice')
        instrumental_select = st.selectbox('Select by instrumental/voice:', ['Instrumental', 'Voice'])
        st.write('## 🔀 Post-process')
        max_tracks = st.number_input('Maximum number of tracks (0 for all):', value=0)
        shuffle = st.checkbox('Random shuffle')

        if st.button("RUN"):
            st.write('## 🔊 Results')
            mp3s = list(instrumental_analysis.index)

            instrumental_analysis_query = instrumental_analysis.loc[mp3s]
            result = instrumental_analysis_query
            result = result.loc[(result['Instrumental/Voice'] == instrumental_select)]
            st.write(result)
            mp3s = result.index

            ut.display_tracks(mp3s, max_tracks, shuffle, m3u_filepath=f'playlists/{instrumental_select}_playlist.m3u8')

    if playlist_option == "Danceability":

        min_danceability = 0
        max_danceability = 1

        st.write('# 💃 Playlist by danceability')
        danceability_select = st.slider('Select by danceability:', min_value=min_danceability, max_value=max_danceability, value=(min_danceability, max_danceability))
        st.write('## 🔝 Rank')
        danceability_rank = st.selectbox('Rank by danceability:', ['Ascending', 'Descending'])
        st.write('## 🔀 Post-process')
        max_tracks = st.number_input('Maximum number of tracks (0 for all):', value=0)
        shuffle = st.checkbox('Random shuffle')

        if st.button("RUN"):
            st.write('## 🔊 Results')
            mp3s = list(danceability_analysis.index)

            danceability_analysis_query = danceability_analysis.loc[mp3s]
            result = danceability_analysis_query
            result = result.loc[(result['danceability'] >= danceability_select[0]) & (result['danceability'] <= danceability_select[1])]
            st.write(result)
            mp3s = result.index

            if danceability_rank == 'Ascending':
                danceability_analysis_query = danceability_analysis.loc[mp3s]
                ranked = danceability_analysis_query.sort_values(['danceability'], ascending=[True])
                mp3s = list(ranked.index)
                st.write('Applied ranking by danceability.')
                st.write(ranked)
            elif danceability_rank == 'Descending':
                danceability_analysis_query = danceability_analysis.loc[mp3s]
                ranked = danceability_analysis_query.sort_values(['danceability'], ascending=[False])
                mp3s = list(ranked.index)
                st.write('Applied ranking by danceability.')
                st.write(ranked)

            ut.display_tracks(mp3s, max_tracks, shuffle, m3u_filepath='playlists/danceability_playlist.m3u8')
            
    if playlist_option == "Arousal-Valence":

        min_value = 1
        max_value = 9

        st.write('## 🥵 Filter by arousal and valence')
        arousal_select = st.slider('Select by arousal:', min_value=min_value, max_value=max_value, value=(min_value, max_value))
        valence_select = st.slider('Select by valence:', min_value=min_value, max_value=max_value, value=(min_value, max_value))
        st.write('## 🔝 Rank')
        arousal_valence_rank = st.selectbox('Rank by:', ['Ascending arousal', 'Descending arousal', 'Ascending valence', 'Descending valence'])
        st.write('## 🔀 Post-process')
        max_tracks = st.number_input('Maximum number of tracks (0 for all):', value=0)
        shuffle = st.checkbox('Random shuffle')

        if st.button("RUN"):
            st.write('## 🔊 Results')
            mp3s = list(arousal_valence_analysis.index)

            arousal_valence_analysis_query = arousal_valence_analysis.loc[mp3s]
            result = arousal_valence_analysis_query
            result = result.loc[(result['arousal'] >= arousal_select[0]) & (result['arousal'] <= arousal_select[1])
                                & (result['valence'] >= valence_select[0]) & (result['valence'] <= valence_select[1])]
            st.write(result)
            mp3s = result.index

            if arousal_valence_rank == 'Ascending arousal':
                arousal_valence_analysis_query = arousal_valence_analysis.loc[mp3s]
                ranked = arousal_valence_analysis_query.sort_values(['arousal'], ascending=[True])
                mp3s = list(ranked.index)
                st.write('Applied ranking by arousal.')
                st.write(ranked)
            elif arousal_valence_rank == 'Descending arousal':
                arousal_valence_analysis_query = arousal_valence_analysis.loc[mp3s]
                ranked = arousal_valence_analysis_query.sort_values(['arousal'], ascending=[False])
                mp3s = list(ranked.index)
                st.write('Applied ranking by arousal.')
                st.write(ranked)
            elif arousal_valence_rank == 'Ascending valence':
                arousal_valence_analysis_query = arousal_valence_analysis.loc[mp3s]
                ranked = arousal_valence_analysis_query.sort_values(['valence'], ascending=[True])
                mp3s = list(ranked.index)
                st.write('Applied ranking by valence.')
                st.write(ranked)
            elif arousal_valence_rank == 'Descending valence':
                arousal_valence_analysis_query = arousal_valence_analysis.loc[mp3s]
                ranked = arousal_valence_analysis_query.sort_values(['valence'], ascending=[False])
                mp3s = list(ranked.index)
                st.write('Applied ranking by valence.')
                st.write(ranked)

            ut.display_tracks(mp3s, max_tracks, shuffle, m3u_filepath='playlists/arousal_valence_playlist.m3u8')

    if playlist_option == "Key and Scale":

        st.write('# 🎹 Filter by Key and Scale')
        key_select = st.selectbox('Select by key:', ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])
        scale_select = st.selectbox('Select by scale:', ['major', 'minor'])
        profile_select = st.selectbox('Select by profile:', ['Temperley', 'Krumhansl', 'Edma'])
        st.write('## 🔀 Post-process')
        max_tracks = st.number_input('Maximum number of tracks (0 for all):', value=0)
        shuffle = st.checkbox('Random shuffle')

        if st.button("RUN"):
            st.write('## 🔊 Results')
            mp3s = list(key_scale_analysis.index)
            if profile_select == 'Temperley':
                key_scale_analysis_query = key_scale_analysis.loc[mp3s]['keyTemperley']
            elif profile_select == 'Krumhansl':
                key_scale_analysis_query = key_scale_analysis.loc[mp3s]['keyKrumhansl']
            elif profile_select == 'Edma':
                key_scale_analysis_query = key_scale_analysis.loc[mp3s]['keyEdma']
            
            result = key_scale_analysis_query
            result = result.loc[(result == key_select + ' ' + scale_select)]
            st.write(result)
            mp3s = result.index

            ut.display_tracks(mp3s, max_tracks, shuffle, m3u_filepath=f'playlists/{key_select}_{scale_select}_{profile_select}_playlist.m3u8')