## Audio feature extraction, analysis and music similarity playlists generation using Python and Streamlit

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

Uses [Essentia](http://essentia.upf.edu.) for audio feature extraction and analysis.
[1] Bogdanov, D., Wack N., Gómez E., Gulati S., Herrera P., Mayor O., et al. (2013). ESSENTIA: an Audio Analysis Library for Music Information Retrieval. International Society for Music Information Retrieval Conference (ISMIR'13). 493-498.

Model weights and metadata are obtained from [Essentia models website](https://essentia.upf.edu/models.html)

Sample audio collection used for analysis is obtained from the [MUSAV](https://repositori.upf.edu/handle/10230/54181) dataset.
