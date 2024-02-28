import os.path
import random
import streamlit as st
import utils as ut


m3u_filepaths_file = 'playlists/streamlit.m3u8'
GENRE_ANALYSIS_PATH = 'genre_predictions.csv'
METADATA_FILE_PATH = 'metadata/discogs-effnet-bs64-1.json'
OTHER_FEATURES_PATH = 'features.csv'




playlist_option = st.sidebar.selectbox(
    "Create playlist based on:",
    ["Genre", "Tempo","Instrumental/Voice", "Danceability", "Arousal-Valence", "Key and Scale"],
)

if playlist_option == "Genre":
    genre_analysis, genre_analysis_styles = ut.load_genre_analysis()

    st.write('# Audio analysis playlists example')
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

            #for style in style_select:
            #    fig, ax = plt.subplots()
            #    ax.hist(genre_analysis_query[style], bins=100)
            #    st.pyplot(fig)

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

        if max_tracks:
            mp3s = mp3s[:max_tracks]
            st.write('Using top', len(mp3s), 'tracks from the results.')

        if shuffle:
            random.shuffle(mp3s)
            st.write('Applied random shuffle.')

        # Store the M3U8 playlist.
        with open(m3u_filepaths_file, 'w') as f:
            # Modify relative mp3 paths to make them accessible from the playlist folder.
            mp3_paths = [os.path.join('..', mp3) for mp3 in mp3s]
            f.write('\n'.join(mp3_paths))
            st.write(f'Stored M3U playlist (local filepaths) to `{m3u_filepaths_file}`.')

        st.write('Audio previews for the first 10 results:')
        for mp3 in mp3s[:10]:
            st.audio(mp3, format="audio/mp3", start_time=0)

if playlist_option == "Tempo":

    tempo_analysis = ut.load_tempo_analysis() 
    min_tempo = tempo_analysis['tempo'].min()
    max_tempo = tempo_analysis['tempo'].max()

    st.write('## 🔍 Select')
    tempo_select = st.slider('Select by tempo:', min_value=min_tempo, max_value=max_tempo, value=(min_tempo, max_tempo))
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

        if max_tracks:
            mp3s = mp3s[:max_tracks]
            st.write('Using top', len(mp3s), 'tracks from the results.')

        if shuffle:
            random.shuffle(mp3s)
            st.write('Applied random shuffle.')

        # Store the M3U8 playlist.
        with open(m3u_filepaths_file, 'w') as f:
            # Modify relative mp3 paths to make them accessible from the playlist folder.
            mp3_paths = [os.path.join('..', mp3) for mp3 in mp3s]
            f.write('\n'.join(mp3_paths))
            st.write(f'Stored M3U playlist (local filepaths) to `{m3u_filepaths_file}`.')

        st.write('Audio previews for the first 10 results:')

if playlist_option == "Instrumental/Voice":
    instrumental_analysis = ut.load_instrumental_analysis() 
    st.write('## 🔍 Select')
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

        if max_tracks:
            mp3s = mp3s[:max_tracks]
            st.write('Using top', len(mp3s), 'tracks from the results.')

        if shuffle:
            random.shuffle(mp3s)
            st.write('Applied random shuffle.')

        # Store the M3U8 playlist.
        with open(m3u_filepaths_file, 'w') as f:
            # Modify relative mp3 paths to make them accessible from the playlist folder.
            mp3_paths = [os.path.join('..', mp3) for mp3 in mp3s]
            f.write('\n'.join(mp3_paths))
            st.write(f'Stored M3U playlist (local filepaths) to `{m3u_filepaths_file}`.')

        st.write('Audio previews for the first 10 results:')
        for mp3 in mp3s[:10]:
            st.audio(mp3, format="audio/mp3", start_time=0)

if playlist_option == "Danceability":
    danceability_analysis = ut.load_danceability_analysis() 
    min_danceability = 0
    max_danceability = 1

    st.write('## 🔍 Select')
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

        if max_tracks:
            mp3s = mp3s[:max_tracks]
            st.write('Using top', len(mp3s), 'tracks from the results.')

        if shuffle:
            random.shuffle(mp3s)
            st.write('Applied random shuffle.')

        # Store the M3U8 playlist.
        with open(m3u_filepaths_file, 'w') as f:
            # Modify relative mp3 paths to make them accessible from the playlist folder.
            mp3_paths = [os.path.join('..', mp3) for mp3 in mp3s]
            f.write('\n'.join(mp3_paths))
            st.write(f'Stored M3U playlist (local filepaths) to `{m3u_filepaths_file}`.')

        st.write('Audio previews for the first 10 results:')
        for mp3 in mp3s[:10]:
            st.audio(mp3, format="audio/mp3", start_time=0)
            
if playlist_option == "Arousal-Valence":
    arousal_valence_analysis = ut.load_arousal_valence_analysis()
    min_value = 1
    max_value = 9

    st.write('## 🔍 Select')
    arousal_select = st.slider('Select by arousal:', min_value=min_value, max_value=max_value, value=(min_value, max_value))
    valence_select = st.slider('Select by valence:', min_value=min_value, max_value=max_value, value=(min_value, max_value))
    st.write('## 🔝 Rank')
    arousal_rank = st.selectbox('Rank by arousal:', ['Ascending', 'Descending'])
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

        if danceability_rank == 'Ascending':
            arousal_valence_analysis_query = arousal_valence_analysis.loc[mp3s]
            ranked = arousal_valence_analysis_query.sort_values(['danceability'], ascending=[True])
            mp3s = list(ranked.index)
            st.write('Applied ranking by danceability.')
            st.write(ranked)
        elif danceability_rank == 'Descending':
            arousal_valence_analysis_query = arousal_valence_analysis.loc[mp3s]
            ranked = arousal_valence_analysis_query.sort_values(['danceability'], ascending=[False])
            mp3s = list(ranked.index)
            st.write('Applied ranking by danceability.')
            st.write(ranked)

        if max_tracks:
            mp3s = mp3s[:max_tracks]
            st.write('Using top', len(mp3s), 'tracks from the results.')

        if shuffle:
            random.shuffle(mp3s)
            st.write('Applied random shuffle.')

        # Store the M3U8 playlist.
        with open(m3u_filepaths_file, 'w') as f:
            # Modify relative mp3 paths to make them accessible from the playlist folder.
            mp3_paths = [os.path.join('..', mp3) for mp3 in mp3s]
            f.write('\n'.join(mp3_paths))
            st.write(f'Stored M3U playlist (local filepaths) to `{m3u_filepaths_file}`.')

        st.write('Audio previews for the first 10 results:')
        for mp3 in mp3s[:10]:
            st.audio(mp3, format="audio/mp3", start_time=0)

if playlist_option == "Key and Scale":
    key_scale_analysis = ut.load_key_scale_analysis()
    st.write('## 🔍 Select')
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

        if max_tracks:
            mp3s = mp3s[:max_tracks]
            st.write('Using top', len(mp3s), 'tracks from the results.')

        if shuffle:
            random.shuffle(mp3s)
            st.write('Applied random shuffle.')

        # Store the M3U8 playlist.
        with open(m3u_filepaths_file, 'w') as f:
            # Modify relative mp3 paths to make them accessible from the playlist folder.
            mp3_paths = [os.path.join('..', mp3) for mp3 in mp3s]
            f.write('\n'.join(mp3_paths))
            st.write(f'Stored M3U playlist (local filepaths) to `{m3u_filepaths_file}`.')

        st.write('Audio previews for the first 10 results:')
        for mp3 in mp3s[:10]:
            st.audio(mp3, format="audio/mp3", start_time=0)