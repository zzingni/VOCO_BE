# app/services/audio_service.py
import os
import shutil
from tempfile import NamedTemporaryFile
from app.utils.audio_converter import convert_to_mp3
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def process_audio(file):
    # 1. 임시 파일 저장
    with NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        shutil.copyfileobj(file.file, temp)
        temp_path = temp.name

    # 2. mp3 변환
    mp3_path = convert_to_mp3(temp_path)

    # 3. Whisper STT
    with open(mp3_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file
        )

    print("📝 STT 결과:", transcript.text)

    # 4. 파일 정리
    os.remove(temp_path)
    os.remove(mp3_path)

    return transcript.text