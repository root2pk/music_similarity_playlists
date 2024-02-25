"""
Methods for extracting audio features from audio files
"""

import os
# Set logging level for tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}

import essentia
# # Set logging level for essentia
essentia.log.warningActive = False               # deactivate the warning level
essentia.log.infoActive = False                  # deactivate the info level

import essentia.standard as es
import logging



class EssentiaClasses:
    def __init__(self):
       
        # Initialise the classes
        self.getRhythm = es.RhythmExtractor2013()
        self.getKeyTemperley = es.KeyExtractor(profileType='temperley')
        self.getKeyKrumhansl = es.KeyExtractor(profileType='krumhansl')
        self.getKeyEdma = es.KeyExtractor(profileType='edma')
        self.getLoudness = es.LoudnessEBUR128()
        self.getDiscogsEmbeddings = es.TensorflowPredictEffnetDiscogs(graphFilename="weights/discogs-effnet-bs64-1.pb", output="PartitionedCall:1")
        self.getMusiCNNEmbeddings = es.TensorflowPredictMusiCNN(graphFilename="weights/msd-musicnn-1.pb", output="model/dense/BiasAdd")
        self.getMusicStyles = es.TensorflowPredict2D(graphFilename="weights/genre_discogs400-discogs-effnet-1.pb", input="serving_default_model_Placeholder", output="PartitionedCall:0")
        self.getInstrumental = es.TensorflowPredict2D(graphFilename="weights/voice_instrumental-discogs-effnet-1.pb", output="model/Softmax")
        self.getDanceability = es.TensorflowPredict2D(graphFilename="weights/danceability-discogs-effnet-1.pb", output="model/Softmax")
        self.getArousalAndValence = es.TensorflowPredict2D(graphFilename="weights/emomusic-msd-musicnn-2.pb", output="model/Identity")

    def extract_features(self, audio_mono, audio_stereo):
        """
        Extract audio features from an audio file

        Parameters:
        audio_file (str): The path to the audio file

        Returns:
        None
        """

        # Get features
        self.tempo = self.getRhythm(audio_mono)[0]
        self.keyTemperley, self.scaleTemperley, _= self.getKeyTemperley(audio_mono)
        self.keyKrumhansl, self.scaleKrumhansl, _= self.getKeyKrumhansl(audio_mono)
        self.keyEdma, self.scaleEdma, _ = self.getKeyEdma(audio_mono)
        self.loudness = self.getLoudness(audio_stereo)[2]

        # Get embeddings
        discogsEmbeddings = self.getDiscogsEmbeddings(audio_mono)
        musicnnEmbeddings = self.getMusiCNNEmbeddings(audio_mono)

        # Use embeddings on classifier models
        genre_Predictions = self.getMusicStyles(discogsEmbeddings)
        instrVoice = self.getInstrumental(discogsEmbeddings)
        instrumental = instrVoice[:, 0]
        voice = instrVoice[:, 1]
        danceability = self.getDanceability(discogsEmbeddings)[:, 0]
        arouVal = self.getArousalAndValence(musicnnEmbeddings)
        arousal = arouVal[:, 0]
        valence = arouVal[:, 1]

        # Average classifier output frames
        self.genreActivations = genre_Predictions.mean(axis=0)
        self.genre = self.genreActivations.argmax()
        self.instrumental = instrumental.mean(axis=0)
        self.voice = voice.mean(axis=0)
        self.danceability = danceability.mean(axis=0)
        self.arousal = arousal.mean(axis=0)
        self.valence = valence.mean(axis=0)

    def write_features_dict(self, audio_file):
        """
        Write the extracted features to a dictionary

        Parameters:
        audio_file (str): The path to the audio file

        Returns:
        features (dict): A dictionary containing the extracted features

        """

        features = {
            'audio_file': audio_file,
            'tempo': self.tempo,
            'keyTemperley': self.keyTemperley,
            'scaleTemperley': self.scaleTemperley,
            'keyKrumhansl': self.keyKrumhansl,
            'scaleKrumhansl': self.scaleKrumhansl,
            'keyEdma': self.keyEdma,
            'scaleEdma': self.scaleEdma,
            'loudness': self.loudness,
            'instrumentalAvg': self.instrumental,
            'voiceAvg': self.voice,
            'danceabilityAvg': self.danceability,
            'arousalAvg': self.arousal,
            'valenceAvg': self.valence,
        }

        return features
    
    def write_genre_dict(self, audio_file):
        """
        Write the genre predictionas to a dictionary

        Parameters:
        audio_file (str): The path to the audio file

        Returns:
        features (dict): A dictionary containing the genre predictions

        """

        genre_predictions = {
            'audio_file': audio_file,
            'genrePredictions': self.genreActivations,
            'genre': self.genre
        }

        return genre_predictions

def search_audio_files(directory, file_types=['.mp3', '.wav', '.flac', '.aac']):
    """
    Search for audio files in a given directory

    Parameters:
    directory (str): The directory to search for audio files
    file_types (list): The file types to search for

    Returns:
    audio_files (list): A list of the audio files found in the directory

    """

    audio_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(tuple(file_types)):
                audio_files.append(os.path.join(root, file))

    return audio_files

def load_audio_file(file_path):
    """
    Load an audio file from a given path, downmix to mono and resample to 16kHz

    Parameterers:
    file_path (str): The path to the audio file

    Returns:
    audio_stereo (np.array): The audio signal
    audio_mono(np.array): The downmixed audio signal resampled to 16kHz

    """
    # Extract stereo auio
    audio_stereo, sr, nc, _, _, _ =  es.AudioLoader(filename=file_path)()
    # Mix to mono
    audio_mono = es.MonoMixer()(audio_stereo, nc)
    # Resample to 16kHz
    audio_mono = es.Resample(inputSampleRate=44100, outputSampleRate=16000)(audio_mono)

    return audio_stereo, audio_mono

