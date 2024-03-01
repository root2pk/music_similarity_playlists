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

# Define common plotting parameters
title_font_size = 14
axes_label_font_size = 12

# Key order
keyOrder = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
keyScaleOrder = ['C major', 'C minor', 'C# major', 'C# minor', 'D major', 'D minor', 'Eb major', 'Eb minor', 'E major', 'E minor', 'F major', 'F minor', 'F# major', 'F# minor', 'G major', 'G minor', 'Ab major', 'Ab minor', 'A major', 'A minor', 'Bb major', 'Bb minor', 'B major', 'B minor']

def plot_distribution(data, x_col, title, xlabel, ylabel, save_path, kde=False, hist_shrink=1, rotation = 0, figsize = (10,6), hue = None, order = None, rugplot = False):
    """
    Plot and save the distribution of a feature

    Parameters:
    data (pd.DataFrame): The data to be plotted
    x_col (str): The column name to be plotted
    title (str): The title of the plot
    xlabel (str): The x-axis label
    ylabel (str): The y-axis label
    save_path (str): The path to save the plot
    kde (bool): Whether to plot the kernel density estimate
    hist_shrink (float): The amount to shrink the histogram bars
    rotation (int): The rotation of the x-axis labels

    Returns:
    None
    """
    if isinstance(data, pd.Series):
        data = pd.DataFrame({x_col: data})

    # Plot and save the distribution
    plt.figure(figsize=figsize)
    # Order specifically for key and scale plots
    if order:
        sns.countplot(data=data, x=x_col, hue = hue,  order = order)
    else:
        sns.histplot(data=data, x=x_col, kde=kde, shrink=hist_shrink)
    # Rugplot for tempo, loudness, danceability
    if rugplot:
        sns.rugplot(data=data, x=x_col, color='red')

    plt.title(title, fontsize=title_font_size, pad=15)
    plt.xlabel(xlabel, fontsize=axes_label_font_size)
    plt.xticks(rotation=rotation)
    plt.ylabel(ylabel, fontsize=axes_label_font_size)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.clf()


# MAIN -----------------------------------------------------------------------------------------------
# Read features file path
df_features = pd.read_csv(FEATURES_FILE_PATH, header=None)

# Read genre predictions file path and plot distribution of genres
print("Plotting distribution of parent genres...")
df_genres = pd.read_csv(GENRE_PREDICTIONS_FILE_PATH, usecols=[3], header=None)
df_genres.columns = ['Parent Genre']
plot_distribution(df_genres, 'Parent Genre', 'Distribution of Parent Genres', None, 'Number of tracks', 'plots/parent_genre_distribution.png', rotation=45)

# Plot tempo distribution
print("Plotting tempo distribution...")
plot_distribution(df_features[1], 'Tempo', 'Tempo distribution', 'Tempo (bpm)', 'Number of tracks', 'plots/tempo_distribution.png', kde=True, rugplot=True)

# Plot danceability distribution
print("Plotting danceability distribution...")
plot_distribution(df_features[10], 'Danceability', 'Danceability distribution', 'Danceability (0-1)', 'Number of tracks', 'plots/danceability_distribution.png', rugplot=True)

# Plot key distribution only
print("Plotting key distribution for each profile...")
df_key = df_features[[2, 4, 6]].copy()  # Explicitly copy the subset
df_key.columns = ['Temperley', 'Krumhansl', 'Edma']
df_key = df_key.melt(var_name='Profile', value_name='Key')

plot_distribution(df_key, 'Key', 'Key Distribution between profiles', 'Key', 'Number of tracks', 'plots/key_distribution.png', hue = 'Profile', order = keyOrder)

# Plot scale distribution only
print("Plotting scale distribution for each profile...")
df_scale = df_features[[3, 5, 7]].copy()  # Explicitly copy the subset
df_scale.columns = ['Temperley', 'Krumhansl', 'Edma']
df_scale = df_scale.melt(var_name='Profile', value_name='Scale')

plot_distribution(df_scale,'Scale', 'Scale Distribution between profiles', 'Scale', 'Number of tracks', 'plots/scale_distribution.png', hue = 'Profile', order = ['major', 'minor'])

# Plot key and scale distribution
print("Plotting key and scale distribution...")
for profile in ['Temperley', 'Krumhansl', 'Edma']:
    key_col, scale_col = (2, 3) if profile == 'Temperley' else (4, 5) if profile == 'Krumhansl' else (6, 7)
    df_key_scale = df_features[[key_col, scale_col]].copy()  # Explicitly copy the subset
    df_key_scale.columns = ['key', 'scale']
    df_key_scale['Key and Scale'] = df_key_scale['key'] + ' ' + df_key_scale['scale']
    plot_distribution(df_key_scale, 'Key and Scale', f'Key and Scale distribution - {profile}', None, 'Number of tracks', f'plots/key_scale_distribution_{profile.lower()}.png', rotation=45, order = keyScaleOrder)

# Plot loudness distribution
print("Plotting loudness distribution...")
plot_distribution(df_features[8], 'Loudness', 'Loudness distribution', 'Loudness (LUFS)', 'Number of tracks', 'plots/loudness_distribution.png', kde=True, rugplot=True)

# Plot distribution of voice/instrumental tracks
print("Plotting voice/instrumental distribution...")
plot_distribution(df_features[9], 'Voice/Instrumental', 'Distribution of Voice/Instrumental tracks', None, 'Number of tracks', 'plots/voice_instrumental_distribution.png', hist_shrink=0.8)

# Plot arousal and valence distribution
print("Plotting arousal and valence distribution...")
df_arousal_valence = df_features[[11, 12]].copy()          # Explicitly copy the subset
df_arousal_valence.columns = ['Arousal', 'Valence']

# Scatter plot
plt.figure(figsize=(10,10))
ax = sns.scatterplot(data=df_arousal_valence, x='Valence', y='Arousal')
plt.title('Arousal and Valence distribution', fontsize=title_font_size, pad=15)
plt.xlabel('Valence', fontsize=axes_label_font_size)
plt.ylabel('Arousal', fontsize=axes_label_font_size)
plt.xlim(0, 10)
plt.ylim(0, 10)
plt.axvline(x=5, color='r', linestyle='--')
plt.axhline(y=5, color='r', linestyle='--')
# Add labels
for label, x, y in [('positive', 9, 5), ('negative', 1, 5), ('high', 5, 9), ('low', 5, 1), ('neutral', 5, 5)]:
    ax.text(x, y, label, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='white', boxstyle='round'))
plt.tight_layout()
plt.savefig('plots/arousal_valence_distribution.png')
plt.clf()

