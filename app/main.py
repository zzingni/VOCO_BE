# app/main.py
from fastapi import FastAPI
from app.api.v1.endpoints import audio

app = FastAPI()

app.include_router(audio.router, prefix="/api/v1/audio")