from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.interview import Interview
from app.models.answer import Answer
from app.models.sentence_feedback import SentenceFeedback
from app.models.repeated_word import RepeatedWord

router = APIRouter()


@router.get("/reports/all")
def get_all_reports(db: Session = Depends(get_db)):

    interviews = db.query(Interview).all()

    result = []

    for interview in interviews:

        answers_data = []

        for answer in interview.answers:

            feedback = db.query(SentenceFeedback).filter(
                SentenceFeedback.answer_id == answer.id
            ).first()

            words = db.query(RepeatedWord).filter(
                RepeatedWord.answer_id == answer.id
            ).all()

            answers_data.append({
                "answer_id": answer.id,
                "question_id": answer.question_id,
                "question": answer.question.content,
                "text": answer.stt_text,

                "feedback": {
                    "score": feedback.score if feedback else None,
                    "content": feedback.content if feedback else None
                },

                "repeated_words": [
                    {
                        "word": w.word,
                        "count": w.word_count
                    }
                    for w in words
                ]
            })

        result.append({
            "interview_id": interview.id,
            "interview_date": interview.interview_date,
            "answers": answers_data
        })

    return {
        "count": len(result),
        "reports": result
    }