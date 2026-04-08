# app/api/v1/endpoints/audio.py
from fastapi import APIRouter, UploadFile, File
from app.services.audio_service import process_audio

router = APIRouter()

@router.post("/stt")
async def speech_to_text(file: UploadFile = File(...)):
    result = await process_audio(file)
    return {"text": result}