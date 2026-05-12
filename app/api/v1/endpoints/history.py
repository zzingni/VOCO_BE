from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.deps import get_db

from app.models.interview import Interview
from app.models.answer import Answer
from app.models.field import Field
from app.models.sentence_feedback import SentenceFeedback

router = APIRouter()


@router.get("/interview/history")
def get_interview_history(
    db: Session = Depends(get_db)
):

    interviews = db.query(Interview).filter(
        Interview.user_id == 1
    ).all()

    result = []

    for interview in interviews:

        field = db.query(Field).filter(
            Field.id == interview.field_id
        ).first()

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
                "id": field.id,
                "main_category": field.main_category,
                "sub_category": field.sub_category
            } if field else None,

            "average_score":
                round(float(avg_score), 1)
                if avg_score else 0
        })

    return {
        "count": len(result),
        "histories": result
    }