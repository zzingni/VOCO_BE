# app/api/v1/endpoints/audio.py

from fastapi import APIRouter, UploadFile, File
from app.services.audio_service import process_audio
from app.services.analysis_service import analyze_text
from app.services.feedback_service import generate_feedback

router = APIRouter()

@router.post("/stt")
async def stt(file: UploadFile):
    text = await process_audio(file)              # 1. STT
    analysis = await analyze_text(text)           # 2. 분석
    feedback = await generate_feedback(analysis) # 3. 피드백

    return {
        "text": text,
        "analysis": analysis,
        "feedback": feedback
    }

