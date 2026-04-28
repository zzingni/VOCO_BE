# app/api/v1/endpoints/audio.py

from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.services.audio_service import process_audio
from app.services.feedback_service import generate_feedback

from app.models.answer import Answer
from app.models.question import Question
from app.models.sentence_feedback import SentenceFeedback

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
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        return {"error": "Invalid question_id"}

    # 3. STT 처리
    text = await process_audio(file)

    try:
        # 4. Answer 먼저 저장 (id 생성 필요)
        answer = Answer(
            user_id=1,
            question_id=question_id,
            stt_text=text
        )

        db.add(answer)
        db.commit()
        db.refresh(answer)  # 여기서 answer.id 생성됨

        # 5. GPT 피드백 생성
        feedback_result = await generate_feedback(
            question.content,
            text
        )

        # 6. Feedback 저장
        feedback = SentenceFeedback(
            answer_id=answer.id,
            score=feedback_result["score"],
            content=feedback_result["feedback"]
        )

        db.add(feedback)
        db.commit()

    except Exception as e:
        db.rollback()
        return {"error": str(e)}

    # 7. 응답
    return {
        "answer_id": answer.id,
        "question_id": question_id,
        "text": text
    }