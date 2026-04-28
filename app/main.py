# app/main.py
from fastapi import FastAPI
from app.api.v1.endpoints import audio
from app.api.v1.endpoints import db_test

app = FastAPI()

app.include_router(audio.router, prefix="/api/v1/audio")
app.include_router(db_test.router, prefix="/api/v1")