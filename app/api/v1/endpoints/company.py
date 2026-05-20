from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db

from app.db.database import SessionLocal
from app.models.company import Company

router = APIRouter()


@router.get("/company/list")
def get_company(search_query: str = None, db: Session = Depends(get_db)):

    if search_query:
        # '%search_query%' 형태로 검색어가 포함되는 기업들을 조회합니다. (최대 100개 제한)
        companies = db.query(Company).filter(Company.company_name.like(f"%{search_query}%")).limit(100).all()
    else:
        # 검색어가 없을 경우 기본값으로 50개까지 반환합니다.
        companies = db.query(Company).limit(50).all()

    return [
        {
            "company_id": c.company_id,
            "company_name": c.company_name,
            "industry_name": c.industry_name
        }
        for c in companies
    ]