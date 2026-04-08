# app/services/audio_service.py
import os
import shutil
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def process_audio(file):
    # 1. 임시 파일 저장
    with NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        shutil.copyfileobj(file.file, temp)
        temp_path = temp.name


    # 2. Whisper STT
    with open(temp_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file
        )

    print("📝 STT 결과:", transcript.text)

    # 3. 파일 정리
    os.remove(temp_path)

    return transcript.text