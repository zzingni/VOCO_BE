from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.question import Question

router = APIRouter()

@router.get("/questions")
def get_questions():
    db: Session = SessionLocal()

    questions = db.query(Question).filter(Question.field_id == 1).all()

    result = [
        {
            "id": q.id,
            "field_id": q.field_id,
            "content": q.content
        }
        for q in questions
    ]

    db.close()
    return result