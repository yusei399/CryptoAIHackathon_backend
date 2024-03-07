from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from functions import predict_features

app = FastAPI()

@app.get("/")
def root():
    return {"message":"CryptoAIHackathon_backend"}

@app.post("/api/v1/recommendations")
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


@app.post("/api/v1/recommendations2")
async def create_upload_files(file: UploadFile = File(...)):

    input_audio_features = await predict_features(file)
    print(input_audio_features)
    return {"message":"CryptoAIHackathon_backend"}