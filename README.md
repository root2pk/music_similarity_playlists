

`main.py` runs the main script to load and extract all the features from the dataset. It runs a loop through the audio files, loads them, and extracts features from them.
Features, genre activation values, predicted genres and predicted parent genres are written into .csv files.
Additionally, the number of predictions for each genre is also written into a separate tsv file. These are stored in the `data\` directory

`methods.py` is a helper file for the main script.

`stats.py` analyses the extracted features and plots the relevant data. Plots are stored in the `plots\` directory.

`app.py`
Streamlit app to create playlists based on the extracted features. Features to be used can be selected using the sidebar. The user can then filter through their requirements for each feature and create separate playlists. The welcome page has an option of running main.py and stats.py once the user uploads their own dataset.

`app2.py`
Streamlit app used to compute tracks similar to a query track. Uses cosine similarity to calculate similarity and displays the top 10 tracks. Tracks can be queried with a search box or drop down menu. 

`utils.py` is the helper file for the apps.

`extract_embeddings.py`
This script extracts embeddings from the models, and ideally should be integrated into main.py.
