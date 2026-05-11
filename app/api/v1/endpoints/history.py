from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.deps import get_db

from app.models.interview import Interview
from app.models.answer import Answer
from app.models.question import Question
from app.models.field import Field
from app.models.sentence_feedback import SentenceFeedback

router = APIRouter()


@router.get("/interview/history")
def get_interview_history(db: Session = Depends(get_db)):

    interviews = db.query(Interview).all()

    result = []

    for interview in interviews:

        # 해당 면접의 답변들
        answers = db.query(Answer).filter(
            Answer.interview_id == interview.id
        ).all()

        if not answers:
            continue

        # 첫 질문 기준으로 분야 가져오기
        first_question = db.query(Question).filter(
            Question.id == answers[0].question_id
        ).first()

        field = None

        if first_question:
            field = db.query(Field).filter(
                Field.id == first_question.field_id
            ).first()

        # 평균 점수 계산
        avg_score = db.query(
            func.avg(SentenceFeedback.score)
        ).join(
            Answer,
            SentenceFeedback.answer_id == Answer.id
        ).filter(
            Answer.interview_id == interview.id
        ).scalar()

        result.append({
            "interview_id": interview.id,

            "interview_date": interview.interview_date,

            "field": {
                "id": field.id if field else None,
                "main_category": field.main_category if field else None,
                "sub_category": field.sub_category if field else None
            },

            "average_score": round(float(avg_score), 1) if avg_score else 0
        })

    return {
        "count": len(result),
        "histories": result
    }