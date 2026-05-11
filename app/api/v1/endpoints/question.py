from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.question import Question

router = APIRouter()


@router.get("/questions")
def get_questions(fieldId: int):
    db: Session = SessionLocal()

    try:
        questions = (
            db.query(Question)
            .filter(Question.field_id == fieldId)
            .all()
        )

        result = [
            {
                "id": q.id,
                "field_id": q.field_id,
                "content": q.content
            }
            for q in questions
        ]

        return result

    finally:
        db.close()