import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from scipy.io import wavfile
import requests
from pydub import AudioSegment
import io

# YAMNetモデルのロード
yamnet_model = hub.load('https://tfhub.dev/google/yamnet/1')

# モデルの読み込み
#model = load('music_recommendation_model.joblib')

async def predict_features(file):
    file_contents = await file.read()
    # MP3からWAVへの変換
    sound = AudioSegment.from_file(io.BytesIO(file_contents), format=file.filename.split('.')[-1])
    temp_wav_path = 'temp_music_preview.wav'
    sound.export(temp_wav_path, format="wav")

    # WAVファイルの読み込み
    sample_rate, wav_data = wavfile.read(temp_wav_path)
    waveform = np.mean(wav_data, axis=1)  # ステレオからモノラルに変換
    waveform = waveform / np.iinfo(wav_data.dtype).max  # 正規化

    # 特徴量の抽出
    _, embeddings, _ = yamnet_model(waveform)
    return embeddings.numpy()

# Spotify APIを使用して音楽を検索し、推薦する関数
def recommend_music(sp, music_attributes, limit=10):
    """
    Spotify APIを使用して音楽を検索し、推薦する関数。類似度スコアを含む。
    """
    # マッピングされた音楽属性をクエリに変換
    query = ' '.join(f'{key}:{value}' for key, value in music_attributes.items())

    # Spotify APIで音楽を検索
    results = sp.search(q=query, limit=limit, type='track')

    # 検索結果からトラック情報を抽出
    tracks = results['tracks']['items']
    recommended_tracks = []
    for track in tracks:
        # トラックの音楽属性を取得
        track_features = sp.audio_features(track['id'])[0]

        # 類似度スコアの計算（ユークリッド距離の逆数を使用）
        similarity_score = 1 / (1 + sum((music_attributes[key] - track_features[key])**2 for key in music_attributes))

        track_info = {
            'id': track['id'],
            'name': track['name'],
            'artists': ', '.join(artist['name'] for artist in track['artists']),
            'url': track['external_urls']['spotify'],
            'similarity_score': similarity_score
        }
        recommended_tracks.append(track_info)

    # 類似度スコアでソートして返す
    recommended_tracks.sort(key=lambda x: x['similarity_score'], reverse=True)
    return recommended_tracks