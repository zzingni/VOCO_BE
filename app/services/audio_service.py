from dotenv import load_dotenv

from app.core.openai_client import client

load_dotenv()


async def process_audio(audio_path: str):

    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file
        )

    print("📝 STT 결과:", transcript.text)

    return transcript.text