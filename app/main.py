from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from functions import (predict_features, predict_attributes, recommend_music)

app = FastAPI()

origins = [
    "https://crypto-ai-hackathon.vercel.app/",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message":"MoodTune_Backend"}

@app.post("/api/v1/recommendation")
async def music_recommendation(file: UploadFile = File(...)):
    input_audio_features = await predict_features(file)
    predicted_attributes = predict_attributes(input_audio_features)
    music_ids = recommend_music(predicted_attributes)
    return JSONResponse(content={"music_id": music_ids[0],"predicted_attributes":predicted_attributes})