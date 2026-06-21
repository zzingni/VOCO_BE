from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.deps import get_db
from app.models.resume import Resume
from app.models.member import Member

router = APIRouter()

@router.post("/resume/save")
async def save_resume(
    member_id: int,
    personality: str,
    motivation: str,
    problem_experience: str,
    aspiration: str,
    db: Session = Depends(get_db)
):

    member = (
        db.query(Member)
        .filter(Member.id == member_id)
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="사용자를 찾을 수 없습니다."
        )

    resume = (
        db.query(Resume)
        .filter(Resume.member_id == member_id)
        .first()
    )

    if resume:

        resume.personality = personality
        resume.motivation = motivation
        resume.problem_experience = problem_experience
        resume.aspiration = aspiration
        resume.updated_at = datetime.utcnow()

        message = "자기소개서 수정 완료"

    else:

        resume = Resume(
            member_id=member_id,
            personality=personality,
            motivation=motivation,
            problem_experience=problem_experience,
            aspiration=aspiration,
            created_at=datetime.utcnow()
        )

        db.add(resume)

        message = "자기소개서 저장 완료"

    db.commit()

    return {
        "message": message
    }


@router.get("/resume/{member_id}")
async def get_resume(
    member_id: int,
    db: Session = Depends(get_db)
):

    resume = (
        db.query(Resume)
        .filter(Resume.member_id == member_id)
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="자기소개서가 존재하지 않습니다."
        )

    return {
        "personality": resume.personality,
        "motivation": resume.motivation,
        "problem_experience": resume.problem_experience,
        "aspiration": resume.aspiration
    }