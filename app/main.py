from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from functions import (predict_features, predict_attributes, recommend_music)

app = FastAPI()

@app.get("/")
def root():
    return {"message":"CryptoAIHackathon_backend"}

@app.post("/api/v1/recommendations2")
def create_recommendation(audio: UploadFile = File(...)):
    # 音声データを処理するためのダミー関数
    # 実際の実装では、音声データを解析して音楽IDを決定します
    def process_audio(audio_file):
        # ここに音声データの処理ロジックを実装
        # 今回はダミーの音楽IDを返します
        return "0kdqcbwei4MDWFEX5f33yG"

    # 音声ファイルを処理
    music_id = process_audio(audio.file.read())

    # 音楽IDをレスポンスとして返す
    return JSONResponse(content={"music_id": music_id})


@app.post("/api/v1/recommendations")
async def music_recommendation(file: UploadFile = File(...)):
    input_audio_features = await predict_features(file)
    predicted_attributes = predict_attributes(input_audio_features)
    music_ids = recommend_music(predicted_attributes)
    return JSONResponse(content={"music_id": music_ids[0],"predicted_attributes":predicted_attributes})