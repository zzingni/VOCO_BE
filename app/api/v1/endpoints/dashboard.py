from app.models.interview import Interview
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.deps import get_db

from app.models.interview import Interview
from app.models.answer import Answer
from app.models.sentence_feedback import SentenceFeedback

router = APIRouter()

@router.get("/dashboard")
def get_dashboard_summary(
        db: Session = Depends(get_db)
):
    user_id = 1

    # 1. Total Interviews
    total_interviews = db.query(func.count(Interview.id)).filter(Interview.user_id == user_id).scalar() or 0

    # 2. Average Score
    avg_score_val = db.query(
        func.avg(SentenceFeedback.score)
    ).join(
        Answer,
        SentenceFeedback.answer_id == Answer.id
    ).join(
        Interview,
        Answer.interview_id == Interview.id
    ).filter(
        Interview.user_id == user_id
    ).scalar()

    average_score = round(float(avg_score_val), 1) if avg_score_val is not None else 0

    # 3. Score Change
    latest_interview = db.query(Interview).filter(Interview.user_id == user_id).order_by(
        Interview.interview_date.desc()).first()
    score_change = 0.0

    if latest_interview:
        latest_score = db.query(
            func.avg(SentenceFeedback.score)
        ).join(
            Answer,
            SentenceFeedback.answer_id == Answer.id
        ).filter(
            Answer.interview_id == latest_interview.id
        ).scalar() or 0

        prev_avg_score = db.query(
            func.avg(SentenceFeedback.score)
        ).join(
            Answer,
            SentenceFeedback.answer_id == Answer.id
        ).join(
            Interview,
            Answer.interview_id == Interview.id
        ).filter(
            Interview.user_id == user_id,
            Interview.id != latest_interview.id
        ).scalar()

        if prev_avg_score is not None:
            score_change = round(float(latest_score) - float(prev_avg_score), 1)
        else:
            score_change = 0.0

    # 4. Trend history (up to last 10 interviews)
    history_interviews = db.query(Interview).filter(
        Interview.user_id == user_id
    ).order_by(
        Interview.interview_date.desc()
    ).limit(10).all()

    trend = []
    for intr in reversed(history_interviews):
        score_val = db.query(
            func.avg(SentenceFeedback.score)
        ).join(
            Answer,
            SentenceFeedback.answer_id == Answer.id
        ).filter(
            Answer.interview_id == intr.id
        ).scalar()

        trend.append({
            "interview_id": intr.id,
            "interview_date": intr.interview_date,
            "score": round(float(score_val), 1) if score_val is not None else 0
        })
    return {
        "total_interviews": total_interviews,
        "average_score": average_score,
        "score_change": score_change,
        "trend": trend
    }