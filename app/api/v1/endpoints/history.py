from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

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
    total_score = 0
    valid_score_count = 0
    this_month_count = 0
    
    now = datetime.now()

    for interview in interviews:
        if interview.interview_date and interview.interview_date.year == now.year and interview.interview_date.month == now.month:
            this_month_count += 1

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

        if avg_score:
            total_score += float(avg_score)
            valid_score_count += 1

        result.append({
            "interview_id": interview.id,

            "interview_date": interview.interview_date,

            "company_id": interview.company_id,
            "company_name": interview.company.company_name if interview.company else None,

            "field": {
                "id": field.id,
                "main_category": field.main_category,
                "sub_category": field.sub_category
            } if field else None,

            "average_score":
                round(float(avg_score), 1)
                if avg_score is not None else None
        })

    overall_average = round(total_score / valid_score_count, 1) if valid_score_count > 0 else 0

    return {
        "count": len(result),
        "this_month_count": this_month_count,
        "overall_average": overall_average,
        "histories": result
    }