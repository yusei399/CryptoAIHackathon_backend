import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from scipy.io import wavfile
import requests
from pydub import AudioSegment
import io
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from env import(CLIENT_ID, CLIENT_SECRET)
from joblib import load
import sklearn

# Spotify認証
client_id = CLIENT_ID
client_secret = CLIENT_SECRET

credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=credentials)

# モデルのロード
yamnet_model = hub.load('https://tfhub.dev/google/yamnet/1')
model_danceability = load('model/danceability_model.joblib')
model_energy = load('model/energy_model.joblib')
model_valence = load('model/valence_model.joblib')


async def predict_features(file):
    file_contents = await file.read()
    # MP3からWAVへの変換
    #sound = AudioSegment.from_file(io.BytesIO(file_contents), format=file.filename.split('.')[-1])
    sound = AudioSegment.from_file(io.BytesIO(file_contents), format="webm")
    temp_wav_path = 'temp_music_preview.wav'
    sound.export(temp_wav_path, format="wav")

    # WAVファイルの読み込み
    sample_rate, wav_data = wavfile.read(temp_wav_path)
    #waveform = np.mean(wav_data, axis=1)  # ステレオからモノラルに変換
    if wav_data.ndim == 2:  # 2次元配列の場合（ステレオ）
        waveform = np.mean(wav_data, axis=1)  # ステレオからモノラルに変換
    else:  # 1次元配列の場合（モノラル）
        waveform = wav_data  # そのまま使用
    waveform = waveform / np.iinfo(wav_data.dtype).max  # 正規化

    # 特徴量の抽出
    _, embeddings, _ = yamnet_model(waveform)
    return embeddings.numpy()


def predict_attributes(input_audio_features):
    input_audio_features_averaged = np.mean(input_audio_features, axis=0)
    input_audio_features_averaged_2d = np.expand_dims(input_audio_features_averaged, axis=0)
    predicted_danceability = model_danceability.predict(input_audio_features_averaged_2d)[0]
    predicted_energy = model_energy.predict(input_audio_features_averaged_2d)[0]
    predicted_valence = model_valence.predict(input_audio_features_averaged_2d)[0]
    predicted_attributes = {'danceability': predicted_danceability, 'energy': predicted_energy, 'valence': predicted_valence}
    return predicted_attributes


# Spotify APIを使用して音楽を検索し、推薦する関数
def recommend_music(predicted_attributes):
    # 検索条件を設定
    market = "JP"  # 市場を指定（例：米国）
    limit = 5  # 返される曲の数
    
    results = sp.recommendations(seed_genres=['j-pop','pop','rock','jazz'],  # 例としてジャンルをpopに設定
                                target_danceability=predicted_attributes['danceability'],
                                target_energy=predicted_attributes['energy'],
                                target_valence=predicted_attributes['valence'],
                                limit=limit,
                                market=market)
    track_ids = [track['id'] for track in results['tracks']]
    return track_ids