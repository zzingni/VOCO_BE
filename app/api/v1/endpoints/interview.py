# app/api/v1/endpoints/interview.py

from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.interview import Interview

router = APIRouter()


# 면접 시작
@router.post("/interview/start")
def start_interview(
    db: Session = Depends(get_db),
    field_id: int = Form(...)
):

    interview = Interview(
        user_id=1,
        field_id = field_id
    )

    db.add(interview)
    db.commit()
    db.refresh(interview)

    return {
        "message": "Interview started",
        "interview_id": interview.id
    }


# 면접 종료
@router.post("/interview/end/{interview_id}")
def end_interview(
    interview_id: int,
    db: Session = Depends(get_db)
):

    interview = db.query(Interview).filter(
        Interview.id == interview_id
    ).first()

    if not interview:
        return {
            "error": "Interview not found"
        }

    return {
        "message": "Interview ended",
        "interview_id": interview.id
    }