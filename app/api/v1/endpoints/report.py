from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.deps import get_db

from app.models.interview import Interview
from app.models.answer import Answer
from app.models.sentence_feedback import SentenceFeedback
from app.models.repeated_word import RepeatedWord
from app.models.voice_feedback import VoiceFeedback

router = APIRouter()


@router.get("/reports/latest")
def get_latest_report(
    db: Session = Depends(get_db)
):

    interview = db.query(Interview).filter(
        Interview.user_id == 1
    ).order_by(
        Interview.interview_date.desc()
    ).first()

    if not interview:
        return {
            "error": "No interview found"
        }

    overall_score = db.query(
        func.avg(SentenceFeedback.score)
    ).join(
        Answer,
        SentenceFeedback.answer_id == Answer.id
    ).filter(
        Answer.interview_id == interview.id
    ).scalar()

    # Get Voice Feedback averages for current interview
    overall_voice = db.query(
        func.avg(VoiceFeedback.speed),
        func.avg(VoiceFeedback.pitch)
    ).join(
        Answer,
        VoiceFeedback.answer_id == Answer.id
    ).filter(
        Answer.interview_id == interview.id
    ).first()

    current_speed = round(float(overall_voice[0])) if overall_voice and overall_voice[0] is not None else 0
    current_pitch = round(float(overall_voice[1])) if overall_voice and overall_voice[1] is not None else 0

    if current_speed == 0:
        speed_status = "N/A"
    elif current_speed < 100:
        speed_status = "SLOW"
    elif current_speed <= 150:
        speed_status = "IDEAL"
    else:
        speed_status = "FAST"

    if current_pitch == 0:
        pitch_status = "N/A"
    elif current_pitch < 15:
        pitch_status = "FLAT"
    elif current_pitch <= 40:
        pitch_status = "STABLE"
    else:
        pitch_status = "EXPRESSIVE"

    # Get recent 7 interviews history for speed & pitch
    recent_interviews = db.query(Interview).filter(
        Interview.user_id == interview.user_id
    ).order_by(
        Interview.interview_date.desc()
    ).limit(7).all()

    history_data = []
    for ri in reversed(recent_interviews):
        avg_voice = db.query(
            func.avg(VoiceFeedback.speed),
            func.avg(VoiceFeedback.pitch)
        ).join(
            Answer,
            VoiceFeedback.answer_id == Answer.id
        ).filter(
            Answer.interview_id == ri.id
        ).first()

        history_data.append({
            "interview_id": ri.id,
            "interview_date": ri.interview_date,
            "speaking_speed": round(float(avg_voice[0])) if avg_voice and avg_voice[0] is not None else 0,
            "pitch_variation": round(float(avg_voice[1])) if avg_voice and avg_voice[1] is not None else 0
        })

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

    return {
        "interview_id": interview.id,

        "interview_date": interview.interview_date,

        "company_id": interview.company_id,

        "company_name": interview.company.company_name if interview.company else None,

        "field_name": interview.field.sub_category if interview.field else None,

        "overall_score": round(float(overall_score), 1)
        if overall_score else 0,

        "voice_analysis": {
            "speaking_speed": current_speed,
            "speed_status": speed_status,
            "pitch_variation": current_pitch,
            "pitch_status": pitch_status,
            "history": history_data
        },

        "answers": answers_data
    }


@router.get("/reports/{interview_id}")
def get_report_detail(
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

    overall_score = db.query(
        func.avg(SentenceFeedback.score)
    ).join(
        Answer,
        SentenceFeedback.answer_id == Answer.id
    ).filter(
        Answer.interview_id == interview.id
    ).scalar()

    # Get Voice Feedback averages for current interview
    overall_voice = db.query(
        func.avg(VoiceFeedback.speed),
        func.avg(VoiceFeedback.pitch)
    ).join(
        Answer,
        VoiceFeedback.answer_id == Answer.id
    ).filter(
        Answer.interview_id == interview.id
    ).first()

    current_speed = round(float(overall_voice[0])) if overall_voice and overall_voice[0] is not None else 0
    current_pitch = round(float(overall_voice[1])) if overall_voice and overall_voice[1] is not None else 0

    if current_speed == 0:
        speed_status = "N/A"
    elif current_speed < 100:
        speed_status = "SLOW"
    elif current_speed <= 150:
        speed_status = "IDEAL"
    else:
        speed_status = "FAST"

    if current_pitch == 0:
        pitch_status = "N/A"
    elif current_pitch < 15:
        pitch_status = "FLAT"
    elif current_pitch <= 40:
        pitch_status = "STABLE"
    else:
        pitch_status = "EXPRESSIVE"

    # Get recent 7 interviews history for speed & pitch
    recent_interviews = db.query(Interview).filter(
        Interview.user_id == interview.user_id
    ).order_by(
        Interview.interview_date.desc()
    ).limit(7).all()

    history_data = []
    for ri in reversed(recent_interviews):
        avg_voice = db.query(
            func.avg(VoiceFeedback.speed),
            func.avg(VoiceFeedback.pitch)
        ).join(
            Answer,
            VoiceFeedback.answer_id == Answer.id
        ).filter(
            Answer.interview_id == ri.id
        ).first()

        history_data.append({
            "interview_id": ri.id,
            "interview_date": ri.interview_date,
            "speaking_speed": round(float(avg_voice[0])) if avg_voice and avg_voice[0] is not None else 0,
            "pitch_variation": round(float(avg_voice[1])) if avg_voice and avg_voice[1] is not None else 0
        })

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

    return {
        "interview_id": interview.id,

        "interview_date": interview.interview_date,

        "company_id": interview.company_id,

        "company_name": interview.company.company_name if interview.company else None,

        "field_name": interview.field.sub_category if interview.field else None,

        "overall_score": round(float(overall_score), 1)
        if overall_score else 0,

        "voice_analysis": {
            "speaking_speed": current_speed,
            "speed_status": speed_status,
            "pitch_variation": current_pitch,
            "pitch_status": pitch_status,
            "history": history_data
        },

        "answers": answers_data
    }


