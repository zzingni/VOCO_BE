from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.field import Field

router = APIRouter()


@router.get("/field")
def get_field():
    db: Session = SessionLocal()

    try:
        fields = db.query(Field).all()

        result = [
            {
                "id": f.id,
                "main_category": f.main_category,
                "sub_category" : f.sub_category
            }
            for f in fields
        ]

        return result

    finally:
        db.close()