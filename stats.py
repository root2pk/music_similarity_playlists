"""
This script reads the genre_predictions.csv and features.csv files, plots and saves the distribution of the following features:
- Parent genre
- Tempo
- Danceability
- Key and scale (Temperley, Krumhansl, Edma)
- Loudness
- Arousal and Valence
- Voice/Instrumental
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

FEATURES_FILE_PATH = 'data/features.csv'
GENRE_PREDICTIONS_FILE_PATH = 'data/genre_predictions.csv'

def plot_distribution(data, x_col, title, xlabel, ylabel, save_path, kde=False, hist_shrink=1):
    if isinstance(data, pd.Series):
        data = pd.DataFrame({x_col: data})
    sns.histplot(data=data, x=x_col, kde=kde, shrink=hist_shrink)
    sns.rugplot(data=data, x=x_col)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(save_path)
    plt.clf()

# Define common plotting parameters
title_font_size = 14
axes_label_font_size = 12

# Read features file path
df_features = pd.read_csv(FEATURES_FILE_PATH, header=None)

# Read genre predictions file path and plot distribution of genres
df_genres = pd.read_csv(GENRE_PREDICTIONS_FILE_PATH, usecols=[3], header=None)
df_genres.columns = ['Parent Genre']
plot_distribution(df_genres, 'Parent Genre', 'Distribution of Parent Genres', None, None, 'plots/parent_genre_distribution.png')

# Plot tempo distribution
plot_distribution(df_features[1], 'Tempo', 'Tempo distribution', 'Tempo (bpm)', 'Number of tracks', 'plots/tempo_distribution.png', kde=True)

# Plot danceability distribution
plot_distribution(df_features[10], 'Danceability', 'Danceability distribution', 'Danceability (0-1)', 'Number of tracks', 'plots/danceability_distribution.png', kde=True)

# Plot key and scale distribution
for scale in ['Temperley', 'Krumhansl', 'Edma']:
    key_col, scale_col = (2, 3) if scale == 'Temperley' else (4, 5) if scale == 'Krumhansl' else (6, 7)
    df_key_scale = df_features[[key_col, scale_col]].copy()  # Explicitly copy the subset
    df_key_scale.columns = ['key', 'scale']
    df_key_scale['Key and Scale'] = df_key_scale['key'] + ' ' + df_key_scale['scale']
    plot_distribution(df_key_scale, 'Key and Scale', f'Key and Scale distribution - {scale}', 'Key and Scale', 'Number of tracks', f'plots/key_scale_distribution_{scale.lower()}.png')

# Plot loudness distribution
plot_distribution(df_features[8], 'Loudness', 'Loudness distribution', 'Loudness (LUFS)', 'Number of tracks', 'plots/loudness_distribution.png', kde=True)

# Plot arousal and valence distribution
df_arousal_valence = df_features[[11, 12]].copy()  # Explicitly copy the subset
df_arousal_valence.columns = ['Arousal', 'Valence']
df_arousal_valence['Arousal'] -= 5
df_arousal_valence['Valence'] -= 5

ax = sns.scatterplot(data=df_arousal_valence, x='Valence', y='Arousal')
plt.title('Arousal and Valence distribution', fontsize=title_font_size, pad=15)
plt.xlabel('Valence', fontsize=axes_label_font_size)
plt.ylabel('Arousal', fontsize=axes_label_font_size)
plt.xlim(-4, 4)
plt.ylim(-4, 4)
plt.axvline(x=0, color='r', linestyle='--')
plt.axhline(y=0, color='r', linestyle='--')
for label, x, y in [('positive', 4, 0), ('negative', -4, 0), ('high', 0, 4), ('low', 0, -4), ('neutral', 0, 0)]:
    ax.text(x, y, label, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='white', boxstyle='round'))
plt.savefig('plots/arousal_valence_distribution.png')
plt.clf()

# Plot distribution of voice/instrumental tracks
plot_distribution(df_features[9], 'Voice/Instrumental', 'Distribution of Voice/Instrumental tracks', None, 'Number of tracks', 'plots/voice_instrumental_distribution.png', hist_shrink=0.8)
