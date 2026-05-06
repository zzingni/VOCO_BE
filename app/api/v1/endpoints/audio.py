# app/api/v1/endpoints/audio.py

import os
import shutil

from tempfile import NamedTemporaryFile

from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.services.audio_service import process_audio
from app.services.feedback_service import generate_feedback

from app.services.voice_analysis_service import (
    analyze_voice
)

from app.models.answer import Answer
from app.models.question import Question
from app.models.sentence_feedback import SentenceFeedback
from app.models.voice_feedback import VoiceFeedback

from app.services.repeated_word_service import (
    save_repeated_words
)

router = APIRouter()


@router.post("/stt")
async def stt(
    file: UploadFile = File(...),
    question_id: int = Form(...),
    db: Session = Depends(get_db)
):

    # 1. 파일 검증
    if not file.content_type.startswith("audio/"):
        return {"error": "Invalid file type"}

    # 2. 질문 조회
    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if not question:
        return {"error": "Invalid question_id"}

    # 3. 임시 wav 저장
    with NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as temp:

        shutil.copyfileobj(file.file, temp)

        temp_path = temp.name

    try:

        # 4. STT 처리
        text = await process_audio(temp_path)

        # 5. 음성 분석
        voice_result = await analyze_voice(
            temp_path,
            text
        )

        # 6. Answer 저장
        answer = Answer(
            user_id=1,
            question_id=question_id,
            stt_text=text
        )

        db.add(answer)
        db.commit()
        db.refresh(answer)

        # 반복 단어 저장
        save_repeated_words(
            db,
            answer.id,
            text
        )

        # 7. GPT 문장 피드백 생성
        feedback_result = await generate_feedback(
            question.content,
            text
        )

        # 8. Sentence Feedback 저장
        feedback = SentenceFeedback(
            answer_id=answer.id,
            score=feedback_result["score"],
            content=feedback_result["feedback"]
        )

        db.add(feedback)

        # 9. Voice Feedback 저장
        voice_feedback = VoiceFeedback(
            answer_id=answer.id,

            speed=voice_result["speaking_speed"],

            pitch=voice_result["pitch_variation"],

            energy=voice_result["voice_energy"],

            score=0
        )

        db.add(voice_feedback)

        db.commit()

    except Exception as e:

        db.rollback()

        return {"error": str(e)}

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)

    # 10. 응답
    return {
        "answer_id": answer.id,

        "question_id": question_id,

        "text": text,

        "sentence_feedback": feedback_result,

        "voice_feedback": voice_result
    }