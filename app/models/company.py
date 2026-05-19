from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Company(Base):
    __tablename__ = "company"

    company_id = Column(Integer, primary_key=True)
    company_name = Column(String, nullable=False)
    industry_name = Column(String)