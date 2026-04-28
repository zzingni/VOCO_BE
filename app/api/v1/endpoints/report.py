from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.answer import Answer
from app.models.sentence_feedback import SentenceFeedback
from app.models.repeated_word import RepeatedWord

router = APIRouter()


@router.get("/reports/all")
def get_all_reports(db: Session = Depends(get_db)):

    answers = db.query(Answer).all()

    result = []

    for answer in answers:

        feedback = db.query(SentenceFeedback).filter(
            SentenceFeedback.answer_id == answer.id
        ).first()

        words = db.query(RepeatedWord).filter(
            RepeatedWord.answer_id == answer.id
        ).all()

        result.append({
            "answer": {
                "id": answer.id,
                "text": answer.stt_text,
                "question_id": answer.question_id
            },
            "feedback": {
                "score": feedback.score if feedback else None,
                "content": feedback.content if feedback else None
            },
            "repeated_words": [
                {"word": w.word, "count": w.word_count}
                for w in words
            ]
        })

    return {
        "count": len(result),
        "reports": result
    }